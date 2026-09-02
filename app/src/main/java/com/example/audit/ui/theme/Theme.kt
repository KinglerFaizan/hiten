package com.example.audit.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

private val FuturisticBankColorScheme = darkColorScheme(
    primary = CyberCyan,
    onPrimary = CyberObsidian,
    primaryContainer = CyberDarkSurface,
    onPrimaryContainer = CyberCyan,
    secondary = CyberGold,
    onSecondary = CyberObsidian,
    background = CyberObsidian,
    surface = CyberDarkSurface,
    onBackground = Color(0xFFF1F5F9),
    onSurface = Color(0xFFF8FAFC),
    surfaceVariant = CyberCardSurface,
    onSurfaceVariant = Slate300,
    outline = CyberCardBorder
)

@Composable
fun AuditIntelligenceTheme(
    darkTheme: Boolean = true, // Default to futuristic dark terminal aesthetic
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = FuturisticBankColorScheme,
        content = content
    )
}
