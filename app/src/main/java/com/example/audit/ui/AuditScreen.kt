package com.example.audit.ui

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountBalance
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Dashboard
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material.icons.filled.Gavel
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material.icons.filled.People
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.Radar
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Security
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material.icons.filled.Speed
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.audit.R
import com.example.audit.model.AuditArticle
import com.example.audit.model.AuditClassifier
import com.example.audit.ui.theme.BankingEmerald
import com.example.audit.ui.theme.BankingGold
import com.example.audit.ui.theme.BankingRose
import com.example.audit.ui.theme.BankingTeal
import com.example.audit.ui.theme.BankingViolet
import com.example.audit.ui.theme.CyberCardBorder
import com.example.audit.ui.theme.CyberCardSurface
import com.example.audit.ui.theme.CyberCardSurfaceElevated
import com.example.audit.ui.theme.CyberCrimson
import com.example.audit.ui.theme.CyberCyan
import com.example.audit.ui.theme.CyberDarkSurface
import com.example.audit.ui.theme.CyberElectricBlue
import com.example.audit.ui.theme.CyberGold
import com.example.audit.ui.theme.CyberNeonGreen
import com.example.audit.ui.theme.CyberObsidian
import com.example.audit.ui.theme.CyberViolet
import com.example.audit.ui.theme.Slate100
import com.example.audit.ui.theme.Slate300
import com.example.audit.ui.theme.Slate400
import com.example.audit.ui.theme.Slate500
import com.example.audit.ui.theme.Slate600
import com.example.audit.ui.theme.Slate700
import com.example.audit.ui.theme.Slate800
import com.example.audit.ui.theme.Slate900

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuditScreen(
    viewModel: AuditViewModel,
    modifier: Modifier = Modifier
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    var showWarningsExpanded by remember { mutableStateOf(false) }

    val tabs = remember {
        listOf("All") + AuditClassifier.CATEGORY_ORDER + listOf("Bookmarks")
    }

    // Futuristic Pulsing Glow Animation for Surveillance Indicator
    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val pulseAlpha by infiniteTransition.animateFloat(
        initialValue = 0.4f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulseAlpha"
    )

    Scaffold(
        modifier = modifier
            .fillMaxSize()
            .background(CyberObsidian),
        containerColor = CyberObsidian,
        topBar = {
            TopAppBar(
                title = {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        // Futuristic Holographic Shield Badge
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(RoundedCornerShape(10.dp))
                                .background(
                                    Brush.linearGradient(
                                        listOf(CyberDarkSurface, CyberObsidian)
                                    )
                                )
                                .border(
                                    1.2.dp,
                                    Brush.linearGradient(listOf(Color.White, CyberCyan)),
                                    RoundedCornerShape(10.dp)
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Shield,
                                contentDescription = "Bank Security Emblem",
                                tint = Color.White,
                                modifier = Modifier.size(22.dp)
                            )
                        }

                        Spacer(modifier = Modifier.width(12.dp))

                        Column {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(
                                    text = "AUDIT INTELLIGENCE",
                                    fontFamily = FontFamily.Monospace,
                                    fontWeight = FontWeight.ExtraBold,
                                    letterSpacing = 2.sp,
                                    fontSize = 15.sp,
                                    color = Color.White,
                                    style = MaterialTheme.typography.titleMedium.copy(
                                        shadow = androidx.compose.ui.graphics.Shadow(
                                            color = Color(0x9900E5FF),
                                            offset = Offset(0f, 0f),
                                            blurRadius = 10f
                                        )
                                    )
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(4.dp))
                                        .background(Color.White.copy(alpha = 0.12f))
                                        .border(0.75.dp, Color.White.copy(alpha = 0.6f), RoundedCornerShape(4.dp))
                                        .padding(horizontal = 5.dp, vertical = 1.dp)
                                ) {
                                    Text(
                                        text = "BANK // OS",
                                        fontFamily = FontFamily.Monospace,
                                        fontSize = 8.5.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Color.White
                                    )
                                }
                            }
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier
                                        .size(6.dp)
                                        .clip(CircleShape)
                                        .background(CyberCyan.copy(alpha = pulseAlpha))
                                )
                                Spacer(modifier = Modifier.width(5.dp))
                                Text(
                                    text = "INSTITUTIONAL RISK RADAR // LIVE",
                                    fontFamily = FontFamily.Monospace,
                                    color = Color.White.copy(alpha = 0.85f),
                                    fontSize = 8.5.sp,
                                    fontWeight = FontWeight.Medium,
                                    letterSpacing = 0.8.sp
                                )
                            }
                        }
                    }
                },
                actions = {
                    // Quick High-Priority Alert Filter Toggle
                    IconButton(
                        onClick = { viewModel.toggleHighPriorityOnly() },
                        modifier = Modifier
                            .clip(RoundedCornerShape(8.dp))
                            .background(
                                if (uiState.highPriorityOnly) CyberGold.copy(alpha = 0.25f)
                                else Color.White.copy(alpha = 0.05f)
                            )
                            .border(
                                width = 1.dp,
                                color = if (uiState.highPriorityOnly) CyberGold else Color.White.copy(alpha = 0.2f),
                                shape = RoundedCornerShape(8.dp)
                            )
                    ) {
                        Icon(
                            imageVector = Icons.Default.Bolt,
                            contentDescription = "Filter High Priority Signals",
                            tint = if (uiState.highPriorityOnly) CyberGold else Color.White,
                            modifier = Modifier.size(20.dp)
                        )
                    }

                    // Refresh Button with futuristic progress
                    IconButton(
                        onClick = { viewModel.fetchNews() },
                        enabled = !uiState.isLoading,
                        modifier = Modifier.testTag("refresh_news_button")
                    ) {
                        if (uiState.isLoading) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(20.dp),
                                strokeWidth = 2.dp,
                                color = Color.White
                            )
                        } else {
                            Icon(
                                imageVector = Icons.Default.Refresh,
                                contentDescription = stringResource(R.string.fetch_latest_news),
                                tint = Color.White
                            )
                        }
                    }

                    // Terminal Settings Button
                    IconButton(
                        onClick = { viewModel.setShowSettingsSheet(true) },
                        modifier = Modifier.testTag("open_settings_button")
                    ) {
                        Icon(
                            imageVector = Icons.Default.Settings,
                            contentDescription = stringResource(R.string.search_settings),
                            tint = Color.White
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = CyberDarkSurface
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(CyberObsidian)
        ) {
            // Futuristic Hero Banner HUD
            FuturisticHeroHud(
                articles = uiState.articles,
                highPriorityActive = uiState.highPriorityOnly,
                onToggleHighPriority = { viewModel.toggleHighPriorityOnly() }
            )

            // Terminal Search Bar
            FuturisticSearchBar(
                query = uiState.searchQuery,
                onQueryChange = { viewModel.setSearchQuery(it) },
                onClear = { viewModel.setSearchQuery("") }
            )

            // Futuristic Category Radar Row (Segmented Filter Bar)
            FuturisticCategoryRadar(
                tabs = tabs,
                selectedTab = uiState.selectedTab,
                articles = uiState.articles,
                bookmarkedCount = uiState.bookmarkedUrls.size,
                onSelectTab = { viewModel.setSelectedTab(it) }
            )

            // Status / Source Notices (if warnings exist)
            if (uiState.errors.isNotEmpty()) {
                Card(
                    colors = CardDefaults.cardColors(containerColor = CyberCardSurface),
                    shape = RoundedCornerShape(8.dp),
                    border = androidx.compose.foundation.BorderStroke(1.dp, CyberGold.copy(alpha = 0.3f)),
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 6.dp)
                ) {
                    Column(modifier = Modifier.padding(10.dp)) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable { showWarningsExpanded = !showWarningsExpanded }
                        ) {
                            Icon(
                                imageVector = Icons.Default.Info,
                                contentDescription = "Notice",
                                tint = CyberGold,
                                modifier = Modifier.size(16.dp)
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = "SYSTEM ADVISORY: ${uiState.errors.size} source telemetry notes",
                                style = MaterialTheme.typography.bodySmall.copy(
                                    fontFamily = FontFamily.Monospace,
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 11.sp,
                                    color = CyberGold
                                ),
                                modifier = Modifier.weight(1f)
                            )
                            Icon(
                                imageVector = if (showWarningsExpanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                                contentDescription = "Toggle",
                                tint = Slate400,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                        AnimatedVisibility(visible = showWarningsExpanded) {
                            Column(modifier = Modifier.padding(top = 6.dp)) {
                                uiState.errors.forEach { err ->
                                    Text(
                                        text = "• $err",
                                        style = MaterialTheme.typography.bodySmall.copy(
                                            fontFamily = FontFamily.Monospace,
                                            color = Slate400,
                                            fontSize = 10.sp
                                        ),
                                        modifier = Modifier.padding(vertical = 2.dp)
                                    )
                                }
                            }
                        }
                    }
                }
            }

            // Article Telemetry Feed List
            if (uiState.isLoading && uiState.filteredArticles.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator(
                            color = CyberCyan,
                            strokeWidth = 3.dp,
                            modifier = Modifier.size(48.dp)
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "SCANNING GLOBAL FINANCIAL AUDIT REGISTRIES...",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            fontSize = 12.sp,
                            letterSpacing = 1.sp,
                            color = CyberCyan
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = "Analyzing Basel, RBI, SEC, ECB, and Tier-1 banking controls",
                            fontFamily = FontFamily.Monospace,
                            fontSize = 11.sp,
                            color = Slate500
                        )
                    }
                }
            } else if (uiState.filteredArticles.isEmpty()) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Box(
                            modifier = Modifier
                                .size(64.dp)
                                .clip(CircleShape)
                                .background(CyberCardSurface)
                                .border(1.dp, CyberCardBorder, CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Radar,
                                contentDescription = null,
                                tint = CyberCyan,
                                modifier = Modifier.size(32.dp)
                            )
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "NO AUDIT SIGNALS MATCH CURRENT PARAMETERS",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            fontSize = 12.sp,
                            color = Color.White
                        )
                        Spacer(modifier = Modifier.height(6.dp))
                        Text(
                            text = "Try adjusting your search query, toggling high-priority mode, or relaxing the relevance threshold in settings.",
                            style = MaterialTheme.typography.bodySmall.copy(
                                color = Slate400,
                                fontSize = 12.sp,
                                lineHeight = 18.sp
                            ),
                            modifier = Modifier.padding(horizontal = 16.dp)
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Button(
                            onClick = {
                                viewModel.setSearchQuery("")
                                viewModel.setSelectedTab("All")
                                if (uiState.highPriorityOnly) viewModel.toggleHighPriorityOnly()
                                viewModel.fetchNews()
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = CyberCyan),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text(
                                "RESET SCAN FILTERS",
                                fontFamily = FontFamily.Monospace,
                                fontWeight = FontWeight.Bold,
                                color = CyberObsidian,
                                fontSize = 12.sp
                            )
                        }
                    }
                }
            } else {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .testTag("article_feed_list"),
                    contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    items(uiState.filteredArticles, key = { it.url + it.title }) { article ->
                        FuturisticArticleCard(
                            article = article,
                            onToggleBookmark = { viewModel.toggleBookmark(article.url) },
                            onSelect = { viewModel.setSelectedArticle(article) },
                            onOpenUrl = { openBrowser(context, article.url) },
                            onShare = { shareArticle(context, article) }
                        )
                    }

                    item {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 18.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(CyberDarkSurface.copy(alpha = 0.5f))
                                .border(0.5.dp, CyberCardBorder, RoundedCornerShape(8.dp))
                                .padding(12.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Text(
                                    text = "ENCRYPTED AUDIT INTELLIGENCE SURVEILLANCE ENGINE",
                                    fontFamily = FontFamily.Monospace,
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Bold,
                                    letterSpacing = 1.sp,
                                    color = CyberCyan
                                )
                                Spacer(modifier = Modifier.height(4.dp))
                                Text(
                                    text = "Automated domain scoring via NewsAPI financial streams & verified banking databases.",
                                    fontFamily = FontFamily.Monospace,
                                    fontSize = 9.sp,
                                    color = Slate500
                                )
                            }
                        }
                    }
                }
            }
        }
    }

    // Terminal Configuration Modal (Settings Sheet)
    if (uiState.showSettingsSheet) {
        FuturisticSettingsBottomSheet(
            uiState = uiState,
            onDismiss = { viewModel.setShowSettingsSheet(false) },
            onSave = { key, lookback, size, rel, cats ->
                viewModel.updateSettings(key, lookback, size, rel, cats)
            }
        )
    }

    // Classified Dossier Inspection Modal
    if (uiState.selectedArticle != null) {
        FuturisticDossierDialog(
            article = uiState.selectedArticle!!,
            onDismiss = { viewModel.setSelectedArticle(null) },
            onOpenUrl = { openBrowser(context, uiState.selectedArticle!!.url) }
        )
    }
}

/**
 * Futuristic Hero HUD Header with generated image backdrop & live KPI readouts
 */
@Composable
fun FuturisticHeroHud(
    articles: List<AuditArticle>,
    highPriorityActive: Boolean,
    onToggleHighPriority: () -> Unit,
    modifier: Modifier = Modifier
) {
    val totalCount = articles.size
    val highSeverityCount = articles.count { it.auditRelevance >= 65 || it.categoryScore >= 2 }
    val avgRelevance = if (articles.isNotEmpty()) {
        articles.map { it.auditRelevance }.average().toInt()
    } else 0

    Card(
        colors = CardDefaults.cardColors(containerColor = CyberDarkSurface),
        shape = RoundedCornerShape(12.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, CyberCardBorder),
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 6.dp)
    ) {
        Box(modifier = Modifier.fillMaxWidth()) {
            // Background Image with High-Tech Dark Scrim
            Image(
                painter = painterResource(id = R.drawable.img_futuristic_bank),
                contentDescription = "Futuristic Banking Terminal Command",
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(130.dp)
            )

            // Holographic Dark Gradient Scrim Overlay
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(130.dp)
                    .background(
                        Brush.horizontalGradient(
                            listOf(
                                CyberObsidian.copy(alpha = 0.94f),
                                CyberDarkSurface.copy(alpha = 0.82f),
                                CyberObsidian.copy(alpha = 0.96f)
                            )
                        )
                    )
            )

            // Content on top of background
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(12.dp)
            ) {
                // Header badge
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Default.Dashboard,
                            contentDescription = null,
                            tint = CyberCyan,
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = "COMMAND HUD // GLOBAL SURVEILLANCE",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            fontSize = 11.sp,
                            letterSpacing = 1.sp,
                            color = CyberCyan
                        )
                    }

                    // Status Pill
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(4.dp))
                            .background(CyberNeonGreen.copy(alpha = 0.15f))
                            .border(0.5.dp, CyberNeonGreen.copy(alpha = 0.4f), RoundedCornerShape(4.dp))
                            .padding(horizontal = 6.dp, vertical = 2.dp)
                    ) {
                        Text(
                            text = "ACTIVE",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            fontSize = 9.sp,
                            color = CyberNeonGreen
                        )
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))

                // KPI Telemetry Gauges Row
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    KpiBox(
                        title = "TOTAL STREAMS",
                        value = totalCount.toString(),
                        accentColor = CyberElectricBlue
                    )

                    KpiBox(
                        title = "HIGH IMPACT",
                        value = highSeverityCount.toString(),
                        accentColor = if (highSeverityCount > 0) CyberGold else Slate400
                    )

                    KpiBox(
                        title = "AVG INDEX",
                        value = "$avgRelevance/100",
                        accentColor = CyberCyan
                    )

                    // Quick filter chip
                    Surface(
                        onClick = onToggleHighPriority,
                        shape = RoundedCornerShape(8.dp),
                        color = if (highPriorityActive) CyberGold.copy(alpha = 0.2f) else CyberCardSurfaceElevated,
                        border = androidx.compose.foundation.BorderStroke(
                            1.dp,
                            if (highPriorityActive) CyberGold else CyberCardBorder
                        ),
                        modifier = Modifier.height(48.dp)
                    ) {
                        Column(
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Text(
                                text = "FILTER",
                                fontFamily = FontFamily.Monospace,
                                fontSize = 8.sp,
                                color = if (highPriorityActive) CyberGold else Slate400
                            )
                            Text(
                                text = if (highPriorityActive) "★ ACTIVE" else "HIGH SEV",
                                fontFamily = FontFamily.Monospace,
                                fontWeight = FontWeight.Bold,
                                fontSize = 10.sp,
                                color = if (highPriorityActive) CyberGold else Color.White
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun KpiBox(
    title: String,
    value: String,
    accentColor: Color
) {
    Box(
        modifier = Modifier
            .clip(RoundedCornerShape(8.dp))
            .background(CyberCardSurfaceElevated.copy(alpha = 0.8f))
            .border(0.5.dp, CyberCardBorder, RoundedCornerShape(8.dp))
            .padding(horizontal = 10.dp, vertical = 6.dp)
    ) {
        Column {
            Text(
                text = title,
                fontFamily = FontFamily.Monospace,
                fontSize = 8.sp,
                fontWeight = FontWeight.Medium,
                letterSpacing = 0.5.sp,
                color = Slate400
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = value,
                fontFamily = FontFamily.Monospace,
                fontSize = 14.sp,
                fontWeight = FontWeight.Black,
                color = accentColor
            )
        }
    }
}

/**
 * Terminal-styled search bar with prompt prefix
 */
@Composable
fun FuturisticSearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    onClear: () -> Unit
) {
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        placeholder = {
            Text(
                "QUERY // Regulators, sanctions, control breaches, AI risks...",
                fontFamily = FontFamily.Monospace,
                fontSize = 11.sp,
                color = Slate500
            )
        },
        leadingIcon = {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(start = 12.dp)
            ) {
                Text(
                    text = "SYS>",
                    fontFamily = FontFamily.Monospace,
                    fontWeight = FontWeight.Bold,
                    fontSize = 12.sp,
                    color = CyberCyan
                )
                Spacer(modifier = Modifier.width(4.dp))
                Icon(
                    imageVector = Icons.Default.Search,
                    contentDescription = "Search",
                    tint = CyberCyan,
                    modifier = Modifier.size(16.dp)
                )
            }
        },
        trailingIcon = {
            if (query.isNotEmpty()) {
                IconButton(onClick = onClear) {
                    Icon(
                        imageVector = Icons.Default.Clear,
                        contentDescription = "Clear",
                        tint = Slate400,
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        },
        singleLine = true,
        shape = RoundedCornerShape(10.dp),
        colors = OutlinedTextFieldDefaults.colors(
            focusedBorderColor = CyberCyan,
            unfocusedBorderColor = CyberCardBorder,
            focusedContainerColor = CyberDarkSurface,
            unfocusedContainerColor = CyberDarkSurface,
            focusedTextColor = Color.White,
            unfocusedTextColor = Color.White
        ),
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 4.dp)
            .testTag("search_text_input")
    )
}

/**
 * Futuristic Category Radar (Segmented Telemetry Pills)
 */
@Composable
fun FuturisticCategoryRadar(
    tabs: List<String>,
    selectedTab: String,
    articles: List<AuditArticle>,
    bookmarkedCount: Int,
    onSelectTab: (String) -> Unit
) {
    val scrollState = rememberScrollState()

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .horizontalScroll(scrollState)
            .padding(horizontal = 16.dp, vertical = 6.dp)
            .testTag("category_tab_row"),
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        tabs.forEach { tabName ->
            val isSelected = selectedTab == tabName
            val count = when (tabName) {
                "All" -> articles.size
                "Bookmarks" -> bookmarkedCount
                else -> articles.count { it.category.equals(tabName, ignoreCase = true) }
            }

            val categoryColor = getCategoryColor(tabName)
            val icon = getCategoryIcon(tabName)

            Surface(
                onClick = { onSelectTab(tabName) },
                shape = RoundedCornerShape(8.dp),
                color = if (isSelected) categoryColor.copy(alpha = 0.18f) else CyberDarkSurface,
                border = androidx.compose.foundation.BorderStroke(
                    1.dp,
                    if (isSelected) categoryColor else CyberCardBorder
                ),
                modifier = Modifier
                    .height(36.dp)
                    .testTag("tab_$tabName")
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(horizontal = 10.dp)
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = if (isSelected) categoryColor else Slate400,
                        modifier = Modifier.size(15.dp)
                    )

                    Spacer(modifier = Modifier.width(6.dp))

                    Text(
                        text = tabName,
                        fontFamily = FontFamily.Monospace,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                        fontSize = 11.sp,
                        color = if (isSelected) Color.White else Slate400
                    )

                    Spacer(modifier = Modifier.width(6.dp))

                    // Monospace count indicator
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(4.dp))
                            .background(
                                if (isSelected) categoryColor.copy(alpha = 0.25f)
                                else CyberCardSurfaceElevated
                            )
                            .padding(horizontal = 5.dp, vertical = 1.dp)
                    ) {
                        Text(
                            text = count.toString(),
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            fontSize = 10.sp,
                            color = if (isSelected) categoryColor else Slate400
                        )
                    }
                }
            }
        }
    }
}

/**
 * Futuristic Audit Intelligence Article Card
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun FuturisticArticleCard(
    article: AuditArticle,
    onToggleBookmark: () -> Unit,
    onSelect: () -> Unit,
    onOpenUrl: () -> Unit,
    onShare: () -> Unit
) {
    val categoryColor = getCategoryColor(article.category)

    val relevanceColor = when {
        article.auditRelevance >= 75 -> CyberCrimson
        article.auditRelevance >= 50 -> CyberGold
        else -> CyberCyan
    }

    val riskLevel = when {
        article.auditRelevance >= 75 -> "CRITICAL"
        article.auditRelevance >= 50 -> "ELEVATED"
        else -> "MONITOR"
    }

    Card(
        colors = CardDefaults.cardColors(containerColor = CyberCardSurface),
        shape = RoundedCornerShape(12.dp),
        border = androidx.compose.foundation.BorderStroke(1.dp, CyberCardBorder),
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onSelect() }
            .testTag("article_card_${article.title.take(15).replace(" ", "_")}")
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            // Card Header: Category Chip + Monospace Relevance Meter + Bookmark
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.fillMaxWidth()
            ) {
                // Category Chip
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(categoryColor.copy(alpha = 0.15f))
                        .border(0.75.dp, categoryColor.copy(alpha = 0.4f), RoundedCornerShape(4.dp))
                        .padding(horizontal = 7.dp, vertical = 3.dp)
                ) {
                    Text(
                        text = "// ${article.category.uppercase()}",
                        fontFamily = FontFamily.Monospace,
                        color = categoryColor,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold
                    )
                }

                Spacer(modifier = Modifier.width(8.dp))

                // Relevance Score HUD Gauge Pill
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(relevanceColor.copy(alpha = 0.12f))
                        .border(0.75.dp, relevanceColor.copy(alpha = 0.45f), RoundedCornerShape(4.dp))
                        .padding(horizontal = 7.dp, vertical = 3.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        ScoreCircularMeter(
                            score = article.auditRelevance,
                            color = relevanceColor,
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(modifier = Modifier.width(5.dp))
                        Text(
                            text = "$riskLevel ${article.auditRelevance}/100",
                            fontFamily = FontFamily.Monospace,
                            color = relevanceColor,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }

                Spacer(modifier = Modifier.weight(1f))

                IconButton(
                    onClick = onToggleBookmark,
                    modifier = Modifier.size(30.dp)
                ) {
                    Icon(
                        imageVector = if (article.isBookmarked) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                        contentDescription = "Bookmark",
                        tint = if (article.isBookmarked) CyberGold else Slate500,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            // Article Title
            Text(
                text = article.title,
                style = MaterialTheme.typography.titleMedium.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp,
                    lineHeight = 22.sp
                ),
                color = Color.White,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis
            )

            Spacer(modifier = Modifier.height(6.dp))

            // Source and Timestamp
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = article.sourceName.uppercase(),
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = CyberElectricBlue
                )
                Text(
                    text = " // ",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    color = Slate600
                )
                Text(
                    text = formatDateTime(article.publishedAt),
                    fontFamily = FontFamily.Monospace,
                    fontSize = 10.sp,
                    color = Slate400
                )
            }

            if (article.description.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = article.description,
                    style = MaterialTheme.typography.bodySmall.copy(
                        fontSize = 12.sp,
                        lineHeight = 18.sp,
                        color = Slate300
                    ),
                    maxLines = 3,
                    overflow = TextOverflow.Ellipsis
                )
            }

            // Triggered Audit Keywords
            if (article.matchedTerms.isNotEmpty()) {
                Spacer(modifier = Modifier.height(10.dp))
                FlowRow(
                    horizontalArrangement = Arrangement.spacedBy(5.dp),
                    verticalArrangement = Arrangement.spacedBy(4.dp)
                ) {
                    article.matchedTerms.take(4).forEach { term ->
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(4.dp))
                                .background(CyberCardSurfaceElevated)
                                .border(0.5.dp, CyberCyan.copy(alpha = 0.3f), RoundedCornerShape(4.dp))
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        ) {
                            Text(
                                text = "#${term.replace(" ", "_").uppercase()}",
                                fontFamily = FontFamily.Monospace,
                                fontSize = 9.sp,
                                color = CyberCyan,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Bottom Actions
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    // Read Original Article
                    if (article.url.isNotEmpty()) {
                        Button(
                            onClick = onOpenUrl,
                            shape = RoundedCornerShape(6.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = CyberCyan),
                            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                            modifier = Modifier
                                .height(32.dp)
                                .testTag("read_original_button")
                        ) {
                            Text(
                                text = "ORIGINAL SOURCE",
                                fontFamily = FontFamily.Monospace,
                                fontSize = 10.sp,
                                fontWeight = FontWeight.Bold,
                                color = CyberObsidian
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Icon(
                                imageVector = Icons.Default.OpenInNew,
                                contentDescription = null,
                                tint = CyberObsidian,
                                modifier = Modifier.size(12.dp)
                            )
                        }
                    }

                    // View Telemetry Dossier Button
                    OutlinedButton(
                        onClick = onSelect,
                        shape = RoundedCornerShape(6.dp),
                        colors = ButtonDefaults.outlinedButtonColors(contentColor = CyberElectricBlue),
                        border = androidx.compose.foundation.BorderStroke(0.75.dp, CyberCardBorder),
                        contentPadding = PaddingValues(horizontal = 10.dp, vertical = 4.dp),
                        modifier = Modifier.height(32.dp)
                    ) {
                        Text(
                            text = "DOSSIER",
                            fontFamily = FontFamily.Monospace,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }

                IconButton(
                    onClick = onShare,
                    modifier = Modifier.size(32.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Share,
                        contentDescription = "Share",
                        tint = Slate400,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
        }
    }
}

/**
 * Micro Circular Gauge for scores
 */
@Composable
fun ScoreCircularMeter(
    score: Int,
    color: Color,
    modifier: Modifier = Modifier
) {
    Canvas(modifier = modifier) {
        val stroke = 2.dp.toPx()
        // Draw background ring
        drawCircle(
            color = color.copy(alpha = 0.25f),
            radius = size.minDimension / 2 - stroke / 2,
            style = Stroke(width = stroke)
        )
        // Draw progress arc
        val sweepAngle = (score.toFloat() / 100f) * 360f
        drawArc(
            color = color,
            startAngle = -90f,
            sweepAngle = sweepAngle,
            useCenter = false,
            topLeft = Offset(stroke / 2, stroke / 2),
            size = Size(size.width - stroke, size.height - stroke),
            style = Stroke(width = stroke, cap = StrokeCap.Round)
        )
    }
}

/**
 * Futuristic Settings Modal (Terminal Configuration Sheet)
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FuturisticSettingsBottomSheet(
    uiState: AuditUiState,
    onDismiss: () -> Unit,
    onSave: (String, Int, Int, Int, Set<String>) -> Unit
) {
    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    var tempApiKey by remember { mutableStateOf(uiState.apiKey) }
    var tempLookback by remember { mutableFloatStateOf(uiState.lookbackDays.toFloat()) }
    var tempPageSize by remember { mutableFloatStateOf(uiState.pageSize.toFloat()) }
    var tempMinRelevance by remember { mutableFloatStateOf(uiState.minRelevance.toFloat()) }
    var tempCategories by remember { mutableStateOf(uiState.selectedCategories) }

    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = sheetState,
        containerColor = CyberDarkSurface,
        scrimColor = CyberObsidian.copy(alpha = 0.8f)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp)
                .padding(bottom = 32.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        imageVector = Icons.Default.Settings,
                        contentDescription = null,
                        tint = CyberCyan,
                        modifier = Modifier.size(20.dp)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "TERMINAL ENGINE CONFIG",
                        fontFamily = FontFamily.Monospace,
                        fontWeight = FontWeight.Black,
                        fontSize = 16.sp,
                        letterSpacing = 1.sp,
                        color = Color.White
                    )
                }
                IconButton(onClick = onDismiss) {
                    Icon(
                        imageVector = Icons.Default.Close,
                        contentDescription = "Close",
                        tint = Slate400
                    )
                }
            }

            Spacer(modifier = Modifier.height(14.dp))

            // NewsAPI Key Field
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Default.Lock,
                    contentDescription = null,
                    tint = CyberGold,
                    modifier = Modifier.size(14.dp)
                )
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    text = "NEWSAPI ENGINE CREDENTIAL",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = Slate300
                )
            }
            Spacer(modifier = Modifier.height(4.dp))
            OutlinedTextField(
                value = tempApiKey,
                onValueChange = { tempApiKey = it },
                placeholder = {
                    Text(
                        "Leave empty for Curated Banking Intel Feed",
                        fontFamily = FontFamily.Monospace,
                        fontSize = 11.sp,
                        color = Slate500
                    )
                },
                singleLine = true,
                shape = RoundedCornerShape(8.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = CyberCyan,
                    unfocusedBorderColor = CyberCardBorder,
                    focusedContainerColor = CyberCardSurface,
                    unfocusedContainerColor = CyberCardSurface,
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White
                ),
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp)
                    .testTag("settings_api_key_input")
            )

            Spacer(modifier = Modifier.height(12.dp))

            // Lookback days slider
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "TELEMETRY LOOKBACK WINDOW",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = Slate300
                )
                Text(
                    text = "[ ${tempLookback.toInt()} DAYS ]",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = CyberCyan
                )
            }
            Slider(
                value = tempLookback,
                onValueChange = { tempLookback = it },
                valueRange = 1f..7f,
                steps = 5,
                colors = SliderDefaults.colors(
                    thumbColor = CyberCyan,
                    activeTrackColor = CyberCyan,
                    inactiveTrackColor = CyberCardSurfaceElevated
                )
            )

            Spacer(modifier = Modifier.height(8.dp))

            // Articles per category slider
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "ARTICLES PER SURVEILLANCE FEED",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = Slate300
                )
                Text(
                    text = "[ ${tempPageSize.toInt()} STORIES ]",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = CyberElectricBlue
                )
            }
            Slider(
                value = tempPageSize,
                onValueChange = { tempPageSize = it },
                valueRange = 10f..100f,
                steps = 8,
                colors = SliderDefaults.colors(
                    thumbColor = CyberElectricBlue,
                    activeTrackColor = CyberElectricBlue,
                    inactiveTrackColor = CyberCardSurfaceElevated
                )
            )

            Spacer(modifier = Modifier.height(8.dp))

            // Minimum relevance threshold
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "MIN AUDIT RELEVANCE THRESHOLD",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = Slate300
                )
                Text(
                    text = "[ ${tempMinRelevance.toInt()} / 100 ]",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = CyberGold
                )
            }
            Slider(
                value = tempMinRelevance,
                onValueChange = { tempMinRelevance = it },
                valueRange = 5f..50f,
                steps = 8,
                colors = SliderDefaults.colors(
                    thumbColor = CyberGold,
                    activeTrackColor = CyberGold,
                    inactiveTrackColor = CyberCardSurfaceElevated
                )
            )

            Spacer(modifier = Modifier.height(10.dp))

            // Category Feeds Multi-Selector
            Text(
                text = "ACTIVE INTELLIGENCE CATEGORIES",
                fontFamily = FontFamily.Monospace,
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
                color = Slate300
            )
            Spacer(modifier = Modifier.height(4.dp))
            AuditClassifier.CATEGORY_ORDER.forEach { cat ->
                val isChecked = tempCategories.contains(cat)
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable {
                            tempCategories = if (isChecked) {
                                if (tempCategories.size > 1) tempCategories - cat else tempCategories
                            } else {
                                tempCategories + cat
                            }
                        }
                        .padding(vertical = 3.dp)
                ) {
                    Checkbox(
                        checked = isChecked,
                        onCheckedChange = { checked ->
                            tempCategories = if (checked) {
                                tempCategories + cat
                            } else {
                                if (tempCategories.size > 1) tempCategories - cat else tempCategories
                            }
                        },
                        colors = CheckboxDefaults.colors(
                            checkedColor = CyberCyan,
                            checkmarkColor = CyberObsidian,
                            uncheckedColor = Slate500
                        )
                    )
                    Text(
                        text = cat,
                        fontFamily = FontFamily.Monospace,
                        fontSize = 12.sp,
                        color = if (isChecked) Color.White else Slate400
                    )
                }
            }

            Spacer(modifier = Modifier.height(18.dp))

            Button(
                onClick = {
                    onSave(
                        tempApiKey.trim(),
                        tempLookback.toInt(),
                        tempPageSize.toInt(),
                        tempMinRelevance.toInt(),
                        tempCategories
                    )
                },
                shape = RoundedCornerShape(8.dp),
                colors = ButtonDefaults.buttonColors(containerColor = CyberCyan),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp)
                    .testTag("apply_settings_button")
            ) {
                Text(
                    text = "APPLY PARAMETERS & INITIALIZE SYNC",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Bold,
                    color = CyberObsidian
                )
            }
        }
    }
}

/**
 * Futuristic Classified Dossier Inspection Modal
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun FuturisticDossierDialog(
    article: AuditArticle,
    onDismiss: () -> Unit,
    onOpenUrl: () -> Unit
) {
    val categoryColor = getCategoryColor(article.category)

    androidx.compose.ui.window.Dialog(onDismissRequest = onDismiss) {
        Card(
            shape = RoundedCornerShape(14.dp),
            colors = CardDefaults.cardColors(containerColor = CyberDarkSurface),
            border = androidx.compose.foundation.BorderStroke(1.dp, CyberCyan.copy(alpha = 0.5f)),
            elevation = CardDefaults.cardElevation(defaultElevation = 12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(18.dp)
            ) {
                // Header Stamp
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(4.dp))
                            .background(categoryColor.copy(alpha = 0.2f))
                            .border(0.75.dp, categoryColor, RoundedCornerShape(4.dp))
                            .padding(horizontal = 8.dp, vertical = 3.dp)
                    ) {
                        Text(
                            text = "DOSSIER // ${article.category.uppercase()}",
                            fontFamily = FontFamily.Monospace,
                            color = categoryColor,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }

                    IconButton(onClick = onDismiss, modifier = Modifier.size(28.dp)) {
                        Icon(
                            imageVector = Icons.Default.Close,
                            contentDescription = "Close",
                            tint = Slate400
                        )
                    }
                }

                Spacer(modifier = Modifier.height(10.dp))

                Text(
                    text = article.title,
                    style = MaterialTheme.typography.titleMedium.copy(
                        fontWeight = FontWeight.Bold,
                        fontSize = 16.sp,
                        lineHeight = 22.sp
                    ),
                    color = Color.White
                )

                Spacer(modifier = Modifier.height(6.dp))

                Text(
                    text = "FEED: ${article.sourceName.uppercase()} // TS: ${formatDateTime(article.publishedAt)}",
                    fontFamily = FontFamily.Monospace,
                    fontSize = 10.sp,
                    color = CyberElectricBlue
                )

                Spacer(modifier = Modifier.height(12.dp))

                // Score Holographic Telemetry Box
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(8.dp))
                        .background(CyberCardSurface)
                        .border(1.dp, CyberCardBorder, RoundedCornerShape(8.dp))
                        .padding(10.dp),
                    horizontalArrangement = Arrangement.SpaceAround
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = "${article.auditRelevance}/100",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Black,
                            fontSize = 18.sp,
                            color = CyberCyan
                        )
                        Text(
                            text = "AUDIT RELEVANCE",
                            fontFamily = FontFamily.Monospace,
                            fontSize = 9.sp,
                            color = Slate400
                        )
                    }
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = "+${article.categoryScore} HITS",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Black,
                            fontSize = 18.sp,
                            color = CyberGold
                        )
                        Text(
                            text = "CATEGORY WEIGHT",
                            fontFamily = FontFamily.Monospace,
                            fontSize = 9.sp,
                            color = Slate400
                        )
                    }
                }

                if (article.matchedTerms.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(10.dp))
                    Text(
                        text = "TRIGGERED VOCABULARY SIGNALS:",
                        fontFamily = FontFamily.Monospace,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        color = Slate300
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    FlowRow(
                        horizontalArrangement = Arrangement.spacedBy(5.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        article.matchedTerms.forEach { term ->
                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(4.dp))
                                    .background(CyberCyan.copy(alpha = 0.12f))
                                    .border(0.5.dp, CyberCyan.copy(alpha = 0.4f), RoundedCornerShape(4.dp))
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = term.uppercase(),
                                    fontFamily = FontFamily.Monospace,
                                    fontSize = 9.sp,
                                    color = CyberCyan,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                Text(
                    text = article.content ?: article.description,
                    style = MaterialTheme.typography.bodySmall.copy(
                        fontSize = 12.sp,
                        lineHeight = 18.sp,
                        color = Slate300
                    )
                )

                Spacer(modifier = Modifier.height(18.dp))

                if (article.url.isNotEmpty()) {
                    Button(
                        onClick = {
                            onDismiss()
                            onOpenUrl()
                        },
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = CyberCyan),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            text = "OPEN VERIFIED SOURCE",
                            fontFamily = FontFamily.Monospace,
                            fontWeight = FontWeight.Bold,
                            color = CyberObsidian,
                            fontSize = 12.sp
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Icon(
                            imageVector = Icons.Default.OpenInNew,
                            contentDescription = null,
                            tint = CyberObsidian,
                            modifier = Modifier.size(15.dp)
                        )
                    }
                }
            }
        }
    }
}

fun getCategoryColor(category: String): Color {
    return when (category) {
        "Transformation" -> CyberViolet
        "Regulation" -> CyberNeonGreen
        "People" -> CyberGold
        "Cyber and Tech" -> CyberCyan
        "Global Banks" -> CyberElectricBlue
        "Bookmarks" -> CyberGold
        else -> CyberCyan
    }
}

fun getCategoryIcon(category: String): ImageVector {
    return when (category) {
        "All" -> Icons.Default.Dashboard
        "Transformation" -> Icons.Default.Speed
        "Regulation" -> Icons.Default.AccountBalance
        "People" -> Icons.Default.People
        "Cyber and Tech" -> Icons.Default.Security
        "Global Banks" -> Icons.Default.Public
        "Bookmarks" -> Icons.Default.Bookmark
        else -> Icons.Default.Dashboard
    }
}

fun formatDateTime(isoString: String): String {
    if (isoString.isEmpty()) return ""
    return try {
        isoString.take(10)
    } catch (e: Exception) {
        isoString
    }
}

fun openBrowser(context: Context, url: String) {
    if (url.isEmpty()) return
    try {
        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
        context.startActivity(intent)
    } catch (e: Exception) {
        Toast.makeText(context, "Cannot open browser: ${e.message}", Toast.LENGTH_SHORT).show()
    }
}

fun shareArticle(context: Context, article: AuditArticle) {
    try {
        val sendIntent = Intent().apply {
            action = Intent.ACTION_SEND
            putExtra(Intent.EXTRA_TITLE, article.title)
            putExtra(
                Intent.EXTRA_TEXT,
                "${article.title}\n\n${article.description}\n\nSource: ${article.url}"
            )
            type = "text/plain"
        }
        val shareIntent = Intent.createChooser(sendIntent, "Share Banking Audit Story")
        context.startActivity(shareIntent)
    } catch (e: Exception) {
        Toast.makeText(context, "Cannot share: ${e.message}", Toast.LENGTH_SHORT).show()
    }
}
