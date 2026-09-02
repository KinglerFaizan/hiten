package com.example.audit

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import com.example.audit.ui.AuditScreen
import com.example.audit.ui.AuditViewModel
import com.example.audit.ui.theme.AuditIntelligenceTheme

class MainActivity : ComponentActivity() {

    private val viewModel: AuditViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            AuditIntelligenceTheme {
                AuditScreen(viewModel = viewModel)
            }
        }
    }
}
