package com.example.audit.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.audit.BuildConfig
import com.example.audit.data.AuditRepository
import com.example.audit.model.AuditArticle
import com.example.audit.model.AuditClassifier
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class AuditUiState(
    val isLoading: Boolean = false,
    val articles: List<AuditArticle> = emptyList(),
    val filteredArticles: List<AuditArticle> = emptyList(),
    val errors: List<String> = emptyList(),
    val selectedTab: String = "All",
    val searchQuery: String = "",
    val highPriorityOnly: Boolean = false,
    val apiKey: String = BuildConfig.NEWSAPI_KEY,
    val lookbackDays: Int = 3,
    val pageSize: Int = 50,
    val selectedCategories: Set<String> = AuditClassifier.CATEGORIES.keys,
    val minRelevance: Int = 5,
    val bookmarkedUrls: Set<String> = emptySet(),
    val showSettingsSheet: Boolean = false,
    val selectedArticle: AuditArticle? = null
)

class AuditViewModel(
    private val repository: AuditRepository = AuditRepository()
) : ViewModel() {

    private val _uiState = MutableStateFlow(AuditUiState())
    val uiState: StateFlow<AuditUiState> = _uiState.asStateFlow()

    init {
        fetchNews()
    }

    fun fetchNews() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errors = emptyList()) }

            val currentState = _uiState.value
            val (fetchedArticles, warnings) = repository.loadNews(
                apiKey = currentState.apiKey,
                lookbackDays = currentState.lookbackDays,
                pageSize = currentState.pageSize,
                selectedCategories = currentState.selectedCategories,
                minRelevance = currentState.minRelevance
            )

            // Preserve bookmarked status
            val updated = fetchedArticles.map { article ->
                article.copy(isBookmarked = currentState.bookmarkedUrls.contains(article.url))
            }

            _uiState.update { state ->
                state.copy(
                    isLoading = false,
                    articles = updated,
                    errors = warnings
                )
            }
            applyFilters()
        }
    }

    fun setSelectedTab(tab: String) {
        _uiState.update { it.copy(selectedTab = tab) }
        applyFilters()
    }

    fun setSearchQuery(query: String) {
        _uiState.update { it.copy(searchQuery = query) }
        applyFilters()
    }

    fun toggleBookmark(url: String) {
        _uiState.update { state ->
            val updatedBookmarks = if (state.bookmarkedUrls.contains(url)) {
                state.bookmarkedUrls - url
            } else {
                state.bookmarkedUrls + url
            }
            val updatedArticles = state.articles.map { article ->
                if (article.url == url) {
                    article.copy(isBookmarked = updatedBookmarks.contains(url))
                } else {
                    article
                }
            }
            state.copy(bookmarkedUrls = updatedBookmarks, articles = updatedArticles)
        }
        applyFilters()
    }

    fun toggleHighPriorityOnly() {
        _uiState.update { it.copy(highPriorityOnly = !it.highPriorityOnly) }
        applyFilters()
    }

    fun updateSettings(
        apiKey: String,
        lookbackDays: Int,
        pageSize: Int,
        minRelevance: Int,
        selectedCategories: Set<String>
    ) {
        _uiState.update {
            it.copy(
                apiKey = apiKey,
                lookbackDays = lookbackDays,
                pageSize = pageSize,
                minRelevance = minRelevance,
                selectedCategories = selectedCategories,
                showSettingsSheet = false
            )
        }
        fetchNews()
    }

    fun setShowSettingsSheet(show: Boolean) {
        _uiState.update { it.copy(showSettingsSheet = show) }
    }

    fun setSelectedArticle(article: AuditArticle?) {
        _uiState.update { it.copy(selectedArticle = article) }
    }

    private fun applyFilters() {
        val state = _uiState.value
        val tab = state.selectedTab
        val query = state.searchQuery.trim().lowercase()

        val filtered = state.articles.filter { article ->
            val matchesTab = if (tab == "All") {
                true
            } else if (tab == "Bookmarks") {
                article.isBookmarked
            } else {
                article.category.equals(tab, ignoreCase = true)
            }

            val matchesRelevance = article.auditRelevance >= state.minRelevance

            val matchesPriority = if (state.highPriorityOnly) {
                article.auditRelevance >= 65 || article.categoryScore >= 2
            } else {
                true
            }

            val matchesSearch = if (query.isEmpty()) {
                true
            } else {
                article.title.lowercase().contains(query) ||
                        article.description.lowercase().contains(query) ||
                        article.sourceName.lowercase().contains(query) ||
                        article.category.lowercase().contains(query) ||
                        article.matchedTerms.any { it.contains(query) }
            }

            matchesTab && matchesRelevance && matchesPriority && matchesSearch
        }

        _uiState.update { it.copy(filteredArticles = filtered) }
    }
}
