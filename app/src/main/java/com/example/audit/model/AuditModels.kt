package com.example.audit.model

import com.google.gson.annotations.SerializedName

data class AuditArticle(
    val title: String,
    val description: String,
    val content: String? = null,
    val url: String,
    val sourceName: String,
    val publishedAt: String,
    val author: String? = null,
    val category: String,
    val auditRelevance: Int,
    val categoryScore: Int,
    val matchedTerms: List<String> = emptyList(),
    val isBookmarked: Boolean = false
)

data class NewsApiResponse(
    @SerializedName("status") val status: String,
    @SerializedName("totalResults") val totalResults: Int? = null,
    @SerializedName("message") val message: String? = null,
    @SerializedName("articles") val articles: List<NewsApiArticle>? = null
)

data class NewsApiArticle(
    @SerializedName("source") val source: NewsApiSource? = null,
    @SerializedName("author") val author: String? = null,
    @SerializedName("title") val title: String? = null,
    @SerializedName("description") val description: String? = null,
    @SerializedName("url") val url: String? = null,
    @SerializedName("urlToImage") val urlToImage: String? = null,
    @SerializedName("publishedAt") val publishedAt: String? = null,
    @SerializedName("content") val content: String? = null
)

data class NewsApiSource(
    @SerializedName("id") val id: String? = null,
    @SerializedName("name") val name: String? = null
)

data class CategoryDefinition(
    val id: String,
    val displayName: String,
    val query: String
)
