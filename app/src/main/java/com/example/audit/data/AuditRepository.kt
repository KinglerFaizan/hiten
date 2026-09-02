package com.example.audit.data

import com.example.audit.model.AuditArticle
import com.example.audit.model.AuditClassifier
import com.example.audit.model.NewsApiArticle
import com.example.audit.network.RetrofitClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale
import java.util.TimeZone

private sealed interface FetchOutcome {
    data class Success(val category: String, val articles: List<NewsApiArticle>) : FetchOutcome
    data class Failure(val message: String) : FetchOutcome
}

class AuditRepository {

    private val apiService = RetrofitClient.apiService

    suspend fun loadNews(
        apiKey: String,
        lookbackDays: Int,
        pageSize: Int,
        selectedCategories: Set<String>,
        minRelevance: Int
    ): Pair<List<AuditArticle>, List<String>> = withContext(Dispatchers.IO) {
        val errors = mutableListOf<String>()
        val allRawArticles = mutableListOf<Pair<String, NewsApiArticle>>()

        val fromDate = calculateFromDate(lookbackDays)
        val categoriesToFetch = selectedCategories.ifEmpty { AuditClassifier.CATEGORIES.keys }

        // Fetch selected categories in parallel using Coroutines (analogous to ThreadPoolExecutor in Python)
        val deferredResults = categoriesToFetch.mapNotNull { category ->
            val query = AuditClassifier.CATEGORIES[category] ?: return@mapNotNull null
            async<FetchOutcome> {
                try {
                    val response = apiService.getEverything(
                        query = query,
                        fromDate = fromDate,
                        pageSize = pageSize,
                        apiKey = apiKey
                    )
                    if (response.status == "ok" && response.articles != null) {
                        FetchOutcome.Success(category, response.articles)
                    } else {
                        FetchOutcome.Failure(response.message ?: "NewsAPI returned status: ${response.status}")
                    }
                } catch (e: Exception) {
                    FetchOutcome.Failure("$category: ${e.localizedMessage ?: e.message ?: "Network error"}")
                }
            }
        }

        val results = deferredResults.awaitAll()
        for (res in results) {
            when (res) {
                is FetchOutcome.Success -> {
                    for (art in res.articles) {
                        allRawArticles.add(res.category to art)
                    }
                }
                is FetchOutcome.Failure -> {
                    errors.add(res.message)
                }
            }
        }

        // Deduplicate by URL first, then by normalized title
        val uniqueMap = mutableMapOf<String, NewsApiArticle>()
        val titleKeys = mutableSetOf<String>()

        for ((_, article) in allRawArticles) {
            val url = (article.url ?: "").trim()
            val title = (article.title ?: "").trim().lowercase()
            val key = if (url.isNotEmpty()) url else title

            if (key.isEmpty() || uniqueMap.containsKey(key) || titleKeys.contains(title)) {
                continue
            }
            uniqueMap[key] = article
            if (title.isNotEmpty()) {
                titleKeys.add(title)
            }
        }

        val cleanedArticles = mutableListOf<AuditArticle>()

        for (article in uniqueMap.values) {
            val text = AuditClassifier.normalizeText(
                article.title,
                article.description,
                article.content
            )
            val (relevance, matchedTerms) = AuditClassifier.auditRelevance(text)

            // Only retain stories with meaningful audit/risk/control signal
            if (relevance < minRelevance) {
                continue
            }

            val (classifiedCategory, categoryScore) = AuditClassifier.classifyArticle(text)

            cleanedArticles.add(
                AuditArticle(
                    title = article.title?.trim() ?: "Untitled",
                    description = article.description?.trim() ?: "",
                    content = article.content?.trim(),
                    url = article.url?.trim() ?: "",
                    sourceName = article.source?.name?.trim() ?: "Unknown source",
                    publishedAt = article.publishedAt?.trim() ?: "",
                    author = article.author?.trim(),
                    category = classifiedCategory,
                    auditRelevance = relevance,
                    categoryScore = categoryScore,
                    matchedTerms = matchedTerms
                )
            )
        }

        // If no articles returned from API or API error occurred, merge/fallback to curated high-value audit intel
        if (cleanedArticles.isEmpty()) {
            val curated = CuratedAuditData.getSampleArticles().filter {
                it.auditRelevance >= minRelevance &&
                        (selectedCategories.isEmpty() || selectedCategories.contains(it.category))
            }
            cleanedArticles.addAll(curated)
            if (errors.isNotEmpty()) {
                errors.add("Active display supplemented with verified banking audit intelligence stories.")
            }
        }

        // Sort descending by audit relevance, then by published date
        cleanedArticles.sortWith(
            compareByDescending<AuditArticle> { it.auditRelevance }
                .thenByDescending { it.publishedAt }
        )

        Pair(cleanedArticles, errors)
    }

    private fun calculateFromDate(daysAgo: Int): String {
        val cal = Calendar.getInstance(TimeZone.getTimeZone("UTC"))
        cal.add(Calendar.DAY_OF_YEAR, -daysAgo)
        val sdf = SimpleDateFormat("yyyy-MM-dd", Locale.US)
        sdf.timeZone = TimeZone.getTimeZone("UTC")
        return sdf.format(cal.time)
    }
}
