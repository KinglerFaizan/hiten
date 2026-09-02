import os
import re
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import pandas as pd
import requests
import streamlit as st

try:
    from config import API_KEY as CONFIG_API_KEY
except ImportError:
    CONFIG_API_KEY = ""


# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & VISILY EDITORIAL DESIGN SYSTEM
# ---------------------------------------------------------

st.set_page_config(
    page_title="Audit Intel | Financial News, Regulations & Insights",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-End Financial Publishing Theme (Light Editorial, Royal Blue Brand Accents, Visily Mockup Precision)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --brand-blue: #1D4ED8;
        --brand-blue-hover: #1E40AF;
        --brand-blue-light: #EFF6FF;
        --brand-blue-border: #BFDBFE;
        --bg-main: #F8FAFC;
        --bg-surface: #FFFFFF;
        --border-subtle: #E2E8F0;
        --border-strong: #CBD5E1;
        --text-headline: #0F172A;
        --text-body: #334155;
        --text-muted: #64748B;
        --text-subtle: #94A3B8;
        --tag-transformation: #2563EB;
        --tag-regulation: #059669;
        --tag-people: #475569;
        --tag-global: #4338CA;
    }

    /* Base Layout & Clean Canvas */
    .stApp {
        background-color: var(--bg-main) !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        color: var(--text-body) !important;
    }

    /* Hide redundant default Streamlit header bar padding */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1260px !important;
    }

    /* Top Brand & Header Bar */
    .top-brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0 16px 0;
        border-bottom: 1px solid var(--border-subtle);
        margin-bottom: 12px;
        flex-wrap: wrap;
        gap: 14px;
    }
    .brand-mark {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
        cursor: pointer;
    }
    .brand-shield-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 17px;
        box-shadow: 0 2px 6px rgba(29, 78, 216, 0.25);
    }
    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.4px;
    }
    .top-actions-cluster {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .top-nav-link {
        font-size: 13.5px;
        font-weight: 600;
        color: #475569;
        text-decoration: none;
        transition: color 0.15s ease;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .top-nav-link:hover {
        color: var(--brand-blue);
    }
    .bell-icon-badge {
        position: relative;
        font-size: 17px;
        color: #475569;
        cursor: pointer;
    }
    .bell-dot {
        position: absolute;
        top: -2px;
        right: -3px;
        width: 7px;
        height: 7px;
        background-color: #EF4444;
        border-radius: 50%;
        border: 1.5px solid white;
    }
    .user-avatar-circle {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: #E2E8F0;
        border: 1px solid #CBD5E1;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 12px;
        color: #1E293B;
    }

    /* Sub-Navigation Strip */
    .subnav-category-strip {
        display: flex;
        align-items: center;
        gap: 28px;
        padding: 8px 0 14px 0;
        border-bottom: 1px solid var(--border-subtle);
        margin-bottom: 16px;
        overflow-x: auto;
    }
    .subnav-item {
        font-size: 11.5px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: #64748B;
        text-decoration: none;
        transition: color 0.15s ease;
        white-space: nowrap;
    }
    .subnav-item:hover, .subnav-item.active {
        color: var(--brand-blue);
    }

    /* Featured Analysis Hero Card */
    .featured-section-heading {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .featured-section-title {
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
    }
    .featured-archive-link {
        font-size: 13px;
        font-weight: 600;
        color: var(--brand-blue);
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .hero-featured-card {
        position: relative;
        border-radius: 14px;
        overflow: hidden;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 32px;
        background-size: cover;
        background-position: center;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.1);
        margin-bottom: 28px;
    }
    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.2) 0%, rgba(15, 23, 42, 0.88) 75%, rgba(15, 23, 42, 0.96) 100%);
        z-index: 1;
    }
    .hero-content {
        position: relative;
        z-index: 2;
    }
    .hero-tag-badge {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 4px;
        background-color: #2563EB;
        color: #FFFFFF;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
    }
    .hero-headline {
        font-size: 27px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.25;
        letter-spacing: -0.5px;
        margin-bottom: 10px;
        max-width: 820px;
    }
    .hero-byline {
        font-size: 13px;
        color: #CBD5E1;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 500;
    }
    .hero-action-btn {
        position: absolute;
        top: 24px;
        right: 24px;
        z-index: 2;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #FFFFFF;
        width: 36px;
        height: 36px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 16px;
    }

    /* Latest Insights Header */
    .insights-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .insights-title {
        font-size: 19px;
        font-weight: 800;
        color: #0F172A;
    }
    .sort-toggle-pill {
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 13px;
    }
    .sort-tab {
        font-weight: 600;
        color: #64748B;
        cursor: pointer;
    }
    .sort-tab.active {
        color: var(--brand-blue);
        font-weight: 700;
        text-decoration: underline;
        text-underline-offset: 4px;
    }

    /* Insight Article Row Item */
    .insight-row-card {
        background: #FFFFFF;
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        display: flex;
        gap: 18px;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        position: relative;
    }
    .insight-row-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.08);
        transform: translateY(-1px);
    }
    .insight-thumbnail {
        width: 140px;
        height: 105px;
        border-radius: 8px;
        object-fit: cover;
        flex-shrink: 0;
        background-color: #F1F5F9;
    }
    .insight-body {
        flex: 1;
        min-width: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .insight-meta-top {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 6px;
    }
    .badge-tag-transformation {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
        background-color: #EFF6FF;
        color: #2563EB;
        text-transform: uppercase;
    }
    .badge-tag-regulation {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
        background-color: #ECFDF5;
        color: #059669;
        text-transform: uppercase;
    }
    .badge-tag-people {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
        background-color: #F1F5F9;
        color: #475569;
        text-transform: uppercase;
    }
    .badge-tag-global {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
        background-color: #EEF2FF;
        color: #4338CA;
        text-transform: uppercase;
    }
    .insight-date {
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .insight-headline {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.35;
        letter-spacing: -0.2px;
        margin-bottom: 6px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .insight-snippet {
        font-size: 13.5px;
        color: #475569;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .insight-footer-meta {
        font-size: 12px;
        color: #64748B;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .read-article-link {
        font-size: 13px;
        font-weight: 600;
        color: var(--brand-blue);
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .read-article-link:hover {
        text-decoration: underline;
    }

    /* Institutional Sidebar Cards */
    .sidebar-widget-box {
        background: #FFFFFF;
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .widget-header-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .daily-leader-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .leader-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #EFF6FF;
    }
    .leader-name {
        font-size: 14.5px;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.25;
    }
    .leader-role {
        font-size: 12px;
        color: #475569;
        font-weight: 500;
    }
    .leader-org {
        font-size: 11.5px;
        color: var(--brand-blue);
        font-weight: 600;
    }

    /* Trending Topics List */
    .trending-item-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #F1F5F9;
        font-size: 13px;
    }
    .trending-item-row:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }
    .trending-topic-title {
        font-weight: 600;
        color: #1E293B;
        text-decoration: none;
    }
    .trending-count-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #64748B;
        background: #F1F5F9;
        padding: 2px 7px;
        border-radius: 10px;
        font-weight: 600;
    }

    /* Active Filters Card */
    .filter-item-row {
        display: flex;
        justify-content: space-between;
        font-size: 12.5px;
        padding: 4px 0;
    }
    .filter-label {
        color: #64748B;
    }
    .filter-val {
        font-weight: 600;
        color: #0F172A;
    }
    .clear-filters-link {
        display: block;
        text-align: right;
        margin-top: 10px;
        font-size: 12px;
        font-weight: 600;
        color: var(--brand-blue);
        text-decoration: none;
    }

    /* Market Pulse Card */
    .market-ticker-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        padding: 7px 0;
        border-bottom: 1px solid #F1F5F9;
    }
    .ticker-symbol {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 700;
        color: #334155;
    }
    .ticker-figure {
        font-family: 'JetBrains Mono', monospace;
        font-size: 13.5px;
        font-weight: 700;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ticker-positive {
        color: #059669;
        font-size: 11px;
        font-weight: 600;
    }
    .ticker-negative {
        color: #DC2626;
        font-size: 11px;
        font-weight: 600;
    }
    .terminal-link {
        display: block;
        margin-top: 10px;
        text-align: center;
        font-size: 12px;
        font-weight: 600;
        color: var(--brand-blue);
        text-decoration: none;
    }

    /* Audit Intelligence Brief (Newsletter Blue Box) */
    .newsletter-royal-card {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        border-radius: 12px;
        padding: 22px;
        color: #FFFFFF;
        box-shadow: 0 4px 14px rgba(29, 78, 216, 0.25);
    }
    .newsletter-title {
        font-size: 17px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 6px;
    }
    .newsletter-copy {
        font-size: 12.5px;
        color: #DBEAFE;
        line-height: 1.45;
        margin-bottom: 14px;
    }

    /* Footer */
    .editorial-footer {
        margin-top: 50px;
        padding-top: 30px;
        border-top: 1px solid var(--border-subtle);
    }
    .footer-top-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 24px;
    }
    .footer-brand-summary {
        font-size: 12.5px;
        color: #64748B;
        max-width: 320px;
        line-height: 1.5;
        margin-top: 6px;
    }
    .footer-links-group {
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
    }
    .footer-link {
        font-size: 13px;
        font-weight: 500;
        color: #475569;
        text-decoration: none;
    }
    .footer-link:hover {
        color: var(--brand-blue);
    }
    .footer-bottom-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px;
        color: #94A3B8;
        padding-top: 16px;
        border-top: 1px solid #F1F5F9;
        flex-wrap: wrap;
        gap: 10px;
    }

    /* Article Detail Page Elements (Page 2) */
    .article-breadcrumbs {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border-subtle);
    }
    .detail-article-headline {
        font-size: 36px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
        letter-spacing: -0.6px;
        margin-top: 10px;
        margin-bottom: 12px;
    }
    .detail-article-subtitle {
        font-size: 18px;
        color: #475569;
        line-height: 1.5;
        margin-bottom: 16px;
    }
    .detail-byline-bar {
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 13px;
        color: #64748B;
        padding-bottom: 20px;
        margin-bottom: 24px;
        border-bottom: 1px solid var(--border-subtle);
    }
    .detail-hero-img {
        width: 100%;
        height: 380px;
        border-radius: 12px;
        object-fit: cover;
        margin-bottom: 24px;
    }
    .detail-body-text {
        font-size: 16px;
        line-height: 1.75;
        color: #1E293B;
        margin-bottom: 24px;
    }
    .pull-quote-box {
        margin: 28px 0;
        padding: 20px 24px;
        background: #EFF6FF;
        border-left: 4px solid var(--brand-blue);
        border-radius: 0 8px 8px 0;
    }
    .pull-quote-text {
        font-size: 17px;
        font-weight: 600;
        color: #1E3A8A;
        font-style: italic;
        line-height: 1.6;
        margin-bottom: 8px;
    }
    .pull-quote-cite {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        color: #2563EB;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .in-this-article-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 20px;
    }
    .in-article-link {
        font-size: 13px;
        color: #334155;
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
        text-decoration: none;
    }
    .tag-chips-row {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 24px 0;
    }
    .article-topic-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        background: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        padding: 4px 10px;
    }

    /* Search Inputs and Controls */
    .stTextInput>div>div>input {
        border-radius: 24px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        padding: 10px 20px !important;
        font-size: 14px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
    }
    .stButton>button {
        border-radius: 20px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 8px 18px !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. SECTOR DEFINITIONS & INTELLIGENCE VOCABULARY
# ---------------------------------------------------------

CATEGORIES = {
    "Transformation": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance") AND ("digital transformation" OR "modernization" OR "core banking" OR "automation" OR "artificial intelligence" OR "generative AI" OR "cloud")',
        "tag_class": "badge-tag-transformation",
        "color": "#2563EB"
    },
    "Regulation": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "compliance" OR "risk" OR "governance") AND ("regulation" OR "regulatory" OR "supervision" OR "RBI" OR "Basel" OR "AML" OR "KYC" OR "sanctions" OR "prudential" OR "enforcement")',
        "tag_class": "badge-tag-regulation",
        "color": "#059669"
    },
    "People": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "risk" OR "governance" OR "controls") AND ("appointed" OR "appointment" OR "CEO" OR "CFO" OR "CRO" OR "CISO" OR "chief audit" OR "internal audit" OR "audit committee" OR "board")',
        "tag_class": "badge-tag-people",
        "color": "#475569"
    },
    "Global Banking": {
        "query": '("bank" OR "banking group" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance" OR "regulatory") AND ("HSBC" OR "JPMorgan" OR "JPMorgan Chase" OR "Citi" OR "Citigroup" OR "Barclays" OR "Deutsche Bank" OR "UBS" OR "BNP Paribas" OR "Santander" OR "Standard Chartered" OR "Bank of America" OR "Goldman Sachs" OR "Morgan Stanley" OR "Wells Fargo" OR "ING" OR "ICBC" OR "MUFG" OR "Mizuho")',
        "tag_class": "badge-tag-global",
        "color": "#4338CA"
    },
}

AUDIT_TERMS = [
    "internal audit", "external audit", "audit committee", "auditor",
    "audit finding", "audit findings", "internal control", "internal controls",
    "control weakness", "control weaknesses", "control deficiency",
    "control deficiencies", "governance", "risk management", "operational risk",
    "model risk", "compliance", "regulatory", "regulation", "supervision",
    "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
    "sanctions", "fraud", "misconduct", "financial crime", "basel", "sox"
]

CATEGORY_TERMS = {
    "Transformation": [
        "digital transformation", "modernization", "core banking", "automation",
        "artificial intelligence", "generative ai", "genai", "machine learning",
        "cloud", "digital banking", "technology transformation", "operating model",
    ],
    "Regulation": [
        "regulation", "regulatory", "rbi", "basel", "prudential", "supervision",
        "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
        "sanctions", "capital requirements", "regulatory capital", "compliance",
    ],
    "People": [
        "appointed", "appointment", "ceo", "cfo", "cro", "ciso", "chief audit",
        "internal audit", "audit committee", "board", "director", "chairman",
        "leadership", "executive",
    ],
    "Global Banking": [
        "hsbc", "jpmorgan", "jpmorgan chase", "citi", "citigroup", "barclays",
        "deutsche bank", "ubs", "bnpparibas", "bnp paribas", "santander",
        "standard chartered", "bank of america", "goldman sachs", "morgan stanley",
        "wells fargo", "ing", "icbc", "mufg", "mizuho",
    ],
}

# Editorial Default Intelligence Mock Articles (Exact Match to Visily Wireframes for Instant High-End Fidelity)
DEFAULT_EDITORIAL_ARTICLES = [
    {
        "id": "hero-1",
        "category": "Global Banking",
        "title": "Global Banking Resilience: Stress Test Results Indicate Strong Capital Buffers for 2024",
        "description": "Comprehensive supervisory stress tests across major international financial institutions indicate resilient Tier 1 leverage buffers and enhanced liquidity ratios under severe macroeconomic shock scenarios.",
        "source": "Global Banking Forum",
        "author": "James Sterling",
        "publishedAt": "2023-10-28T09:00:00Z",
        "read_time": "8 min read",
        "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1200&q=80",
        "url": "https://www.bis.org/basel_framework/",
        "audit_relevance": 95,
        "tags": ["Basel III", "Capital Adequacy", "Stress Testing", "Internal Audit"],
        "content": """The implementation of Basel III, often referred to as the 'Basel III Endgame', marks the most significant shift in global banking regulation since the 2008 financial crisis. For audit professionals and risk managers, these changes demand a fundamental rethinking of how capital adequacy is measured and reported across diverse jurisdictions.

### Standardized Approaches for Credit Risk
Central to the new framework is the reduction in reliance on internal models. The Basel Committee has introduced a more granular and risk-sensitive standardized approach for credit risk (SA-CR). This move aims to enhance comparability across institutions by narrowing the range of risk-weighted assets (RWA) calculated by banks using their own internal ratings-based (IRB) models.

> "The output floor is perhaps the most transformative element of the new package, ensuring that capital requirements cannot drop below 72.5% of the capital requirement calculated using standardized approaches."
> — BASEL COMMITTEE TECHNICAL MEMO, SECTION 4.2

For the internal audit function, the focus must now shift toward validating the accuracy and completeness of the data inputs that feed into these standardized calculations. Data lineage and governance become paramount when regulatory reporting relies on highly specific asset classification.

### Impact on Operational Risk Frameworks
Another cornerstone of the reform is the replacement of all current approaches for operational risk with a single risk-sensitive Standardized Approach (SMA). The new SMA combines a bank's business indicator—a financial statement-based proxy for size—with a multiplier based on the bank's historical internal loss experience.

- Integration of internal loss data into the capital calculation floor
- Enhanced disclosure requirements for Pillar 3 reporting
- Re-evaluation of leverage ratio buffers for G-SIBs
- Revised market risk boundaries (Fundamental Review of the Trading Book)"""
    },
    {
        "id": "item-1",
        "category": "Transformation",
        "title": "Digital Transformation: How AI-Driven Auditing is Reducing Compliance Risk",
        "description": "Financial institutions are increasingly leveraging machine learning to automate the identification of anomalous transactions and streamline regulatory reporting.",
        "source": "Banking Technology Review",
        "author": "Marcus Chen",
        "publishedAt": "2023-10-25T14:30:00Z",
        "read_time": "6 min read",
        "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80",
        "url": "https://www.federalreserve.gov",
        "audit_relevance": 92,
        "tags": ["AI Audit", "Automation", "Machine Learning", "Compliance Risk"],
        "content": "Leading banks are migrating from retrospective periodic sample checks to real-time continuous algorithmic auditing. This transition has diminished compliance discovery lags by 64% while maintaining strict human-in-the-loop governance."
    },
    {
        "id": "item-2",
        "category": "Regulation",
        "title": "New ESG Disclosure Standards: What Audit Committees Need to Know for Q4",
        "description": "The latest regulatory framework mandates more granular reporting on climate-related financial risks, requiring a shift in internal data collection and assurance frameworks.",
        "source": "Regulatory Assurance Dispatch",
        "author": "Dr. Sarah Jenkins",
        "publishedAt": "2023-10-25T10:15:00Z",
        "read_time": "10 min read",
        "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80",
        "url": "https://www.bis.org",
        "audit_relevance": 88,
        "tags": ["ESG Disclosure", "Audit Committee", "Climate Risk", "Supervision"],
        "content": "With mandatory Scope 1, 2, and 3 disclosure deadlines approaching, board audit committees are demanding that internal audit teams establish verifiable control trails over carbon accounting and sustainable loan covenant tracking."
    },
    {
        "id": "item-3",
        "category": "People",
        "title": "The Talent Gap in Specialized Banking Audit: Strategies for Retention",
        "description": "As the complexity of financial regulations increases, firms are finding it harder to recruit and retain high-level audit professionals with cross-disciplinary quantitative expertise.",
        "source": "Executive Talent Monitor",
        "author": "Claire Beaumont",
        "publishedAt": "2023-10-24T16:45:00Z",
        "read_time": "5 min read",
        "image_url": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=600&q=80",
        "url": "https://www.bloomberg.com",
        "audit_relevance": 78,
        "tags": ["Talent Retention", "Internal Audit", "Executive Leadership", "Board Governance"],
        "content": "Specialized internal auditors possessing both quantitative model validation expertise and supervisory experience command unprecedented compensation premiums as banks compete with fintechs and advisory conglomerates."
    },
    {
        "id": "item-4",
        "category": "Regulation",
        "title": "Cross-Border Regulatory Alignment: EU and US Markets Seek Common Ground",
        "description": "Recent bilateral talks suggest a growing consensus on digital asset oversight and capital requirement parity for multinational banking conglomerates.",
        "source": "Global Financial Gazette",
        "author": "Jonathan Pierce",
        "publishedAt": "2023-10-23T11:20:00Z",
        "read_time": "7 min read",
        "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80",
        "url": "https://www.reuters.com",
        "audit_relevance": 85,
        "tags": ["Cross-Border", "EU-US Alignment", "Prudential Oversight", "Digital Assets"],
        "content": "Supervisory harmonization reduces compliance friction for Tier-1 institutions operating concurrently under ECB single supervisory mechanism and US OCC/Federal Reserve mandates."
    },
    {
        "id": "item-5",
        "category": "Regulation",
        "title": "Basel III End-Game: Navigating the Final Hurdles in Global Capital Requirements",
        "description": "As central banks move toward final implementation, audit teams are identifying key gaps in data quality and risk modeling across standardized credit books.",
        "source": "Prudential Risk Journal",
        "author": "Jonathan Pierce",
        "publishedAt": "2023-10-27T08:00:00Z",
        "read_time": "8 min read",
        "image_url": "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=600&q=80",
        "url": "https://www.bis.org",
        "audit_relevance": 94,
        "tags": ["Basel III", "Capital Floors", "Credit Risk", "Model Validation"],
        "content": "Detailed analysis into the output floor calibration and how Tier 1 capital ratios will adjust once the 72.5% standardized parameter takes mandatory effect across SIFIs."
    },
    {
        "id": "item-6",
        "category": "Global Banking",
        "title": "Market Volatility and the Liquidity Coverage Ratio: Stress Testing in Action",
        "description": "Analysis of how recent market shifts tested the liquidity assumptions of mid-cap commercial banks and the resulting supervisory directives on deposit stickiness.",
        "source": "Treasury & Capital Markets",
        "author": "David Vance",
        "publishedAt": "2023-10-18T15:00:00Z",
        "read_time": "7 min read",
        "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=600&q=80",
        "url": "https://www.ft.com",
        "audit_relevance": 89,
        "tags": ["Liquidity Ratio", "Stress Testing", "Commercial Banking", "Supervision"],
        "content": "Uninsured deposit flight modeling has triggered immediate internal control updates across regional banking treasuries, prompting board risk committees to revise collateral haircuts."
    },
]


# ---------------------------------------------------------
# 3. EXTRACTION & LIVE INGESTION HELPERS
# ---------------------------------------------------------

def get_api_key():
    """Extract NewsAPI key safely without hardcoding."""
    if CONFIG_API_KEY.strip():
        return CONFIG_API_KEY.strip()

    env_key = os.getenv("NEWSAPI_KEY", "").strip()
    if env_key:
        return env_key

    try:
        secret_key = st.secrets.get("API_KEY", "") or st.secrets.get("NEWSAPI_KEY", "")
        if secret_key:
            return str(secret_key).strip()
    except Exception:
        pass

    return ""


def normalize_text(article):
    fields = [
        article.get("title") or "",
        article.get("description") or "",
        article.get("content") or "",
    ]
    return " ".join(fields).lower()


def audit_relevance(text):
    score = 0
    for term in AUDIT_TERMS:
        if term in text:
            score += 5
    for term in [
        "internal audit", "audit committee", "internal controls",
        "control deficiency", "regulatory enforcement", "model risk", "financial crime"
    ]:
        if term in text:
            score += 10
    return min(score, 100)


def classify_article(article):
    text = normalize_text(article)
    scores = {}
    for category, terms in CATEGORY_TERMS.items():
        score = sum(1 for term in terms if term in text)
        scores[category] = score
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        best_category = "Regulation"
    return best_category, scores[best_category]


def fetch_category(category, query, api_key, from_date, page_size):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": api_key,
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "ok":
        raise RuntimeError(payload.get("message", "NewsAPI returned an error."))
    rows = []
    for article in payload.get("articles", []):
        article["_query_category"] = category
        rows.append(article)
    return rows


@st.cache_data(ttl=300, show_spinner=False)
def load_live_news(api_key, lookback_days, page_size):
    from_date = (
        datetime.now(timezone.utc) - timedelta(days=lookback_days)
    ).strftime("%Y-%m-%d")
    all_articles = []
    errors = []

    with ThreadPoolExecutor(max_workers=len(CATEGORIES)) as executor:
        futures = {
            executor.submit(
                fetch_category,
                category,
                settings["query"],
                api_key,
                from_date,
                page_size,
            ): category
            for category, settings in CATEGORIES.items()
        }
        for future in as_completed(futures):
            category = futures[future]
            try:
                all_articles.extend(future.result())
            except Exception as exc:
                errors.append(f"{category}: {exc}")

    unique = {}
    title_keys = set()
    for article in all_articles:
        url = article.get("url") or ""
        title = (article.get("title") or "").strip().lower()
        key = url if url else title
        if not key or key in unique or title in title_keys:
            continue
        unique[key] = article
        title_keys.add(title)

    category_images = {
        "Transformation": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80",
        "Regulation": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=600&q=80",
        "People": "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=600&q=80",
        "Global Banking": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80",
    }

    cleaned = []
    idx = 100
    for article in unique.values():
        text = normalize_text(article)
        relevance = audit_relevance(text)
        if relevance < 5:
            continue
        category, category_score = classify_article(article)
        source = article.get("source") or {}
        img = article.get("urlToImage")
        if not img or not img.startswith("http"):
            img = category_images.get(category, category_images["Regulation"])

        cleaned.append({
            "id": f"live-{idx}",
            "category": category,
            "audit_relevance": relevance,
            "category_score": category_score,
            "title": article.get("title") or "Untitled Financial Intelligence",
            "description": article.get("description") or "Live verified banking surveillance coverage. Follow source link for full institutional documentation.",
            "source": source.get("name") or "Institutional Source",
            "author": article.get("author") or "Banking Bureau",
            "publishedAt": article.get("publishedAt") or "",
            "read_time": "6 min read",
            "image_url": img,
            "url": article.get("url") or "",
            "tags": [category, "Internal Audit", "Supervision"],
            "content": article.get("content") or article.get("description") or "Access primary source dossier for complete verified supervisory data."
        })
        idx += 1

    cleaned.sort(key=lambda x: (x["audit_relevance"], x["publishedAt"]), reverse=True)
    return cleaned, errors


def format_display_date(pub_date_str):
    if not pub_date_str:
        return "Recent"
    try:
        clean_str = pub_date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_str)
        return dt.strftime("%b %d, %Y")
    except Exception:
        return pub_date_str[:10] if len(pub_date_str) >= 10 else "Recent"


# ---------------------------------------------------------
# 4. INITIALIZE SESSION STATE & ACTIVE VIEW MANAGEMENT
# ---------------------------------------------------------

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "ALL INSIGHTS"

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "feed"  # 'feed' | 'article' | 'advanced_search'

if "active_article" not in st.session_state:
    st.session_state.active_article = None

if "sort_order" not in st.session_state:
    st.session_state.sort_order = "Most Recent"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "newsletter_subscribed" not in st.session_state:
    st.session_state.newsletter_subscribed = False


# ---------------------------------------------------------
# 5. SIDEBAR: MISSION CONTROL & CREDENTIAL CONFIG
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; padding: 4px 0 16px 0; border-bottom: 1px solid #E2E8F0;">
        <div style="width: 32px; height: 32px; background: #1D4ED8; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 16px;">🛡️</div>
        <div>
            <div style="font-weight: 800; font-size: 16px; color: #0F172A;">Audit Intel</div>
            <div style="font-size: 11px; color: #64748B; font-family: monospace;">SETTINGS & TELEMETRY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_key = get_api_key()
    user_api_key = st.text_input(
        "NewsAPI Key (Optional)",
        value=api_key,
        type="password",
        placeholder="Enter API key for live feed...",
        help="Reads automatically from Streamlit secrets or config.py if present."
    )
    if user_api_key:
        api_key = user_api_key

    lookback_days = st.slider("Lookback Window (Days)", min_value=1, max_value=14, value=7)
    page_size = st.slider("Ingestion Depth", min_value=10, max_value=80, value=30, step=10)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Sync News", use_container_width=True):
            st.session_state.live_loaded = True
            st.rerun()
    with col_btn2:
        if st.button("Reset View", use_container_width=True):
            st.session_state.view_mode = "feed"
            st.session_state.active_article = None
            st.session_state.search_query = ""
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 11px; color: #64748B; line-height: 1.6;">
        <b>SURVEILLANCE COVERAGE:</b><br/>
        • Basel III/IV Prudential Standards<br/>
        • Federal Reserve, ECB & RBI Supervision<br/>
        • Internal Controls & SOX 404<br/>
        • Executive & Audit Committee Appointments
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 6. DATA INGESTION & PIPELINE
# ---------------------------------------------------------

live_errors = []
if api_key and (st.session_state.get("live_loaded") or "news_data" not in st.session_state):
    with st.spinner("Fetching verified global banking surveillance streams..."):
        articles, live_errors = load_live_news(api_key, lookback_days, page_size)
        if articles:
            st.session_state.news_data = articles
        else:
            st.session_state.news_data = DEFAULT_EDITORIAL_ARTICLES
else:
    if "news_data" not in st.session_state:
        st.session_state.news_data = DEFAULT_EDITORIAL_ARTICLES

all_articles = st.session_state.get("news_data", DEFAULT_EDITORIAL_ARTICLES)


# ---------------------------------------------------------
# 7. HEADER TOP NAVIGATION BAR
# ---------------------------------------------------------

col_top_logo, col_top_search, col_top_nav = st.columns([3, 5, 4])

with col_top_logo:
    st.markdown("""
    <div class="top-brand-bar" style="border-bottom: none; padding: 0;">
        <div class="brand-mark">
            <div class="brand-shield-icon">🛡️</div>
            <div class="brand-title">Audit Intel</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_top_search:
    search_input = st.text_input(
        "Search news, regulations, and insights...",
        value=st.session_state.search_query,
        placeholder="🔍  Search news, regulations, and insights...",
        label_visibility="collapsed"
    )
    if search_input != st.session_state.search_query:
        st.session_state.search_query = search_input
        if search_input.strip():
            st.session_state.view_mode = "feed"

with col_top_nav:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: flex-end; gap: 20px; height: 100%; padding-top: 4px;">
        <a href="#" class="top-nav-link" style="color: #1D4ED8; font-weight: 700;">Dashboard</a>
        <a href="#" class="top-nav-link">Saved</a>
        <a href="#" class="top-nav-link">Explore ▾</a>
        <div class="bell-icon-badge">
            🔔<span class="bell-dot"></span>
        </div>
        <div class="user-avatar-circle">
            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=100&q=80" style="width: 100%; height: 100%; object-fit: cover;" />
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 8px 0 12px 0; border-color: #E2E8F0;' />", unsafe_allow_html=True)


# ---------------------------------------------------------
# 8. SUB-NAVIGATION STRIP & CATEGORY FILTER TABS
# ---------------------------------------------------------

col_subnav, col_adv_btn = st.columns([9, 3])
with col_subnav:
    cat_options = ["ALL INSIGHTS", "TRANSFORMATION", "REGULATION", "PEOPLE", "GLOBAL BANKING"]
    selected_cat_pill = st.radio(
        "Categories",
        options=cat_options,
        index=cat_options.index(st.session_state.selected_category) if st.session_state.selected_category in cat_options else 0,
        horizontal=True,
        label_visibility="collapsed"
    )
    if selected_cat_pill != st.session_state.selected_category:
        st.session_state.selected_category = selected_cat_pill
        st.session_state.view_mode = "feed"
        st.rerun()

with col_adv_btn:
    col_t1, col_t2 = st.columns([1, 1])
    with col_t2:
        adv_filter_active = st.session_state.view_mode == "advanced_search"
        if st.button("⛛ " + ("Close Filters" if adv_filter_active else "ADVANCED FILTERS"), use_container_width=True):
            st.session_state.view_mode = "feed" if adv_filter_active else "advanced_search"
            st.rerun()

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# 9. FILTERING LOGIC
# ---------------------------------------------------------

current_cat = st.session_state.selected_category
if current_cat == "ALL INSIGHTS":
    filtered_articles = all_articles
else:
    filtered_articles = [
        a for a in all_articles
        if a["category"].upper() == current_cat or (current_cat == "GLOBAL BANKING" and a["category"] == "Global Banks")
    ]

# Apply Text Search Filter
if st.session_state.search_query.strip():
    sq = st.session_state.search_query.lower()
    filtered_articles = [
        a for a in filtered_articles
        if sq in a["title"].lower() or sq in a["description"].lower() or sq in a.get("author", "").lower() or sq in a.get("source", "").lower()
    ]


# ---------------------------------------------------------
# 10. ROUTE: ARTICLE DETAIL VIEW (PAGE 2 FROM VISILY)
# ---------------------------------------------------------

if st.session_state.view_mode == "article" and st.session_state.active_article:
    art = st.session_state.active_article
    pub_date = format_display_date(art.get("publishedAt"))
    cat = art.get("category", "Regulation")
    tag_class = CATEGORIES.get(cat, {}).get("tag_class", "badge-tag-regulation")

    # Top Breadcrumbs
    b1, b2 = st.columns([8, 4])
    with b1:
        if st.button("← Back to Feed | Article Details"):
            st.session_state.view_mode = "feed"
            st.session_state.active_article = None
            st.rerun()
    with b2:
        st.markdown("""
        <div style="text-align: right; padding-top: 8px;">
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 11.5px; color: #64748B; cursor: pointer;">🔗 COPY LINK</span>
        </div>
        """, unsafe_allow_html=True)

    col_art_main, col_art_side = st.columns([72, 28])

    with col_art_main:
        st.markdown(f"""
        <div>
            <span class="{tag_class}" style="font-size: 11.5px; padding: 4px 10px;">{cat.upper()}</span>
            <div class="detail-article-headline">{art['title']}</div>
            <div class="detail-article-subtitle">{art['description']}</div>
            <div class="detail-byline-bar">
                <span style="font-weight: 700; color: #0F172A;">{art.get('author') or 'Senior Financial Analyst'}</span>
                <span>•</span>
                <span>{pub_date}</span>
                <span>•</span>
                <span>⏱️ {art.get('read_time', '8 min read')}</span>
            </div>
            <img src="{art.get('image_url')}" class="detail-hero-img" alt="Article Visual" />
            <div class="detail-body-text">
                {art.get('content', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Pull quote block
        st.markdown("""
        <div class="pull-quote-box">
            <div class="pull-quote-text">
                "The output floor is perhaps the most transformative element of the new package, ensuring that capital requirements cannot drop below 72.5% of the capital requirement calculated using standardized approaches."
            </div>
            <div class="pull-quote-cite">BASEL COMMITTEE TECHNICAL MEMO, SECTION 4.2</div>
        </div>
        """, unsafe_allow_html=True)

        # Topic Tags
        tags_html = "".join([f'<span class="article-topic-chip">#{tag}</span>' for tag in art.get("tags", ["Basel III", "Capital Adequacy", "Risk Management"])])
        st.markdown(f"""
        <div class="tag-chips-row">
            {tags_html}
        </div>
        """, unsafe_allow_html=True)

        # Primary source link
        if art.get("url"):
            st.markdown(f"""
            <div style="margin: 20px 0; padding: 14px 18px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 13.5px; color: #475569;">Verified Primary Regulatory Source: <b>{art.get('source', 'Institutional')}</b></span>
                <a href="{art['url']}" target="_blank" style="font-size: 13px; font-weight: 700; color: #2563EB; text-decoration: none;">View Original Dispatch ↗</a>
            </div>
            """, unsafe_allow_html=True)

        # Related Analysis & Insights
        st.markdown("<hr style='margin: 36px 0 24px 0;' />", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 18px; font-weight: 800; color: #0F172A; margin-bottom: 16px;'>Related Analysis & Insights</div>", unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)
        related_pool = [a for a in all_articles if a.get("id") != art.get("id")][:3]
        for col, rel_art in zip([rc1, rc2, rc3], related_pool):
            with col:
                st.markdown(f"""
                <div style="background: white; border: 1px solid #E2E8F0; border-radius: 10px; overflow: hidden; padding: 12px; height: 100%;">
                    <img src="{rel_art.get('image_url')}" style="width: 100%; height: 110px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />
                    <span class="{CATEGORIES.get(rel_art.get('category'), {}).get('tag_class', 'badge-tag-regulation')}" style="font-size: 9.5px;">{rel_art.get('category').upper()}</span>
                    <div style="font-size: 13.5px; font-weight: 700; color: #0F172A; margin-top: 6px; line-height: 1.3;">{rel_art.get('title')[:65]}...</div>
                </div>
                """, unsafe_allow_html=True)

    with col_art_side:
        # In this article widget
        st.markdown("""
        <div class="in-this-article-card">
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 12px;">IN THIS ARTICLE</div>
            <a href="#" class="in-article-link"><span style="color: #2563EB; font-weight: 700;">01</span> Regulatory Context</a>
            <a href="#" class="in-article-link"><span style="color: #2563EB; font-weight: 700;">02</span> The Output Floor</a>
            <a href="#" class="in-article-link"><span style="color: #2563EB; font-weight: 700;">03</span> Risk Management Impact</a>
            <a href="#" class="in-article-link"><span style="color: #2563EB; font-weight: 700;">04</span> Strategic Outlook</a>
        </div>
        """, unsafe_allow_html=True)

        # Daily Leader
        st.markdown("""
        <div class="sidebar-widget-box">
            <div class="widget-header-title">👤 DAILY LEADER</div>
            <div class="daily-leader-row">
                <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80" class="leader-avatar" alt="Elena Vance" />
                <div>
                    <div class="leader-name">Elena Vance</div>
                    <div class="leader-role">Chief Risk Officer</div>
                    <div class="leader-org">Global Banking Forum</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Trending Topics
        st.markdown("""
        <div class="sidebar-widget-box">
            <div class="widget-header-title">📈 TRENDING TOPICS</div>
            <div class="trending-item-row">
                <span class="trending-topic-title">Basel III Implementation</span>
                <span class="trending-count-pill">124</span>
            </div>
            <div class="trending-item-row">
                <span class="trending-topic-title">AI in Internal Audit</span>
                <span class="trending-count-pill">98</span>
            </div>
            <div class="trending-item-row">
                <span class="trending-topic-title">ESG Regulatory Updates</span>
                <span class="trending-count-pill">87</span>
            </div>
            <div class="trending-item-row">
                <span class="trending-topic-title">Cyber Resilience Frameworks</span>
                <span class="trending-count-pill">65</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# 11. ROUTE: ADVANCED SEARCH & FACETED FILTERS (PAGE 3)
# ---------------------------------------------------------

elif st.session_state.view_mode == "advanced_search":
    st.markdown("<div style='font-size: 24px; font-weight: 800; color: #0F172A; margin-bottom: 16px;'>Search Results & Intelligence Explorer</div>", unsafe_allow_html=True)

    col_facets, col_results = st.columns([28, 72])

    with col_facets:
        st.markdown("""
        <div class="sidebar-widget-box" style="margin-bottom: 20px;">
            <div style="font-weight: 700; font-size: 14.5px; color: #0F172A; margin-bottom: 14px;">Filters</div>
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 8px;">CLASSIFICATION</div>
        </div>
        """, unsafe_allow_html=True)

        filter_trans = st.checkbox("Transformation", value=True)
        filter_reg = st.checkbox("Regulation", value=True)
        filter_people = st.checkbox("People", value=True)
        filter_global = st.checkbox("Global Banking", value=True)

        st.markdown("<div style='font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin: 16px 0 8px 0;'>DATE PUBLISHED</div>", unsafe_allow_html=True)
        date_facet = st.radio(
            "Date Published",
            options=["Last 24 Hours", "Last 7 Days", "Last 30 Days", "This Year"],
            index=1,
            label_visibility="collapsed"
        )

        st.markdown("<div style='font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin: 16px 0 8px 0;'>REGION</div>", unsafe_allow_html=True)
        region_facet = st.multiselect(
            "Region",
            options=["North America", "EMEA", "Asia Pacific", "Latin America"],
            default=["North America", "EMEA"],
            label_visibility="collapsed"
        )

        st.markdown("""
        <div style="margin-top: 24px;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 8px;">RECENT SEARCHES</div>
            <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12.5px; color: #2563EB;">
                <span>• Basel III Capital</span>
                <span>• ESG Compliance</span>
                <span>• Cyber Risk</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_results:
        active_cats = []
        if filter_trans: active_cats.append("Transformation")
        if filter_reg: active_cats.append("Regulation")
        if filter_people: active_cats.append("People")
        if filter_global: active_cats.append("Global Banking")

        facet_filtered = [a for a in all_articles if a.get("category") in active_cats or (a.get("category") == "Global Banks" and "Global Banking" in active_cats)]
        if st.session_state.search_query:
            sq = st.session_state.search_query.lower()
            facet_filtered = [a for a in facet_filtered if sq in a["title"].lower() or sq in a["description"].lower()]

        # Results Summary Header Bar
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #E2E8F0; padding-bottom: 12px;">
            <div>
                <span style="font-size: 18px; font-weight: 800; color: #0F172A;">Search Results</span>
                <span style="font-size: 13px; color: #64748B; margin-left: 10px;">Found <b>{len(facet_filtered)}</b> articles</span>
            </div>
            <div style="font-size: 12.5px; color: #64748B;">
                Sort by: <b>Relevance ▾</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for art in facet_filtered:
            cat = art["category"]
            tag_class = CATEGORIES.get(cat, {}).get("tag_class", "badge-tag-regulation")
            pub_date = format_display_date(art.get("publishedAt"))

            col_card_content, col_card_btn = st.columns([85, 15])
            with col_card_content:
                st.markdown(f"""
                <div class="insight-row-card" style="margin-bottom: 12px;">
                    <img src="{art.get('image_url')}" class="insight-thumbnail" alt="thumbnail" />
                    <div class="insight-body">
                        <div>
                            <div class="insight-meta-top">
                                <span class="{tag_class}">{cat.upper()}</span>
                                <span class="insight-date">📅 {pub_date} &nbsp;•&nbsp; ⏱️ {art.get('read_time', '6 min read')}</span>
                            </div>
                            <div class="insight-headline">{art['title']}</div>
                            <div class="insight-snippet">{art['description']}</div>
                        </div>
                        <div class="insight-footer-meta">
                            <span>Source: <b>{art.get('source')}</b></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_card_btn:
                st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
                if st.button("Read", key=f"adv_btn_{art.get('id')}", use_container_width=True):
                    st.session_state.active_article = art
                    st.session_state.view_mode = "article"
                    st.rerun()


# ---------------------------------------------------------
# 12. ROUTE: MAIN EDITORIAL FEED (PAGE 1 FROM VISILY)
# ---------------------------------------------------------

else:
    # Top Featured Analysis (Hero Card)
    featured_art = filtered_articles[0] if filtered_articles else DEFAULT_EDITORIAL_ARTICLES[0]

    st.markdown("""
    <div class="featured-section-heading">
        <div class="featured-section-title">Featured Analysis</div>
        <a href="#" class="featured-archive-link">View Archive ›</a>
    </div>
    """, unsafe_allow_html=True)

    hero_img = featured_art.get("image_url") or "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1200&q=80"
    hero_date = format_display_date(featured_art.get("publishedAt"))

    st.markdown(f"""
    <div class="hero-featured-card" style="background-image: url('{hero_img}');">
        <div class="hero-overlay"></div>
        <div class="hero-action-btn">🔖</div>
        <div class="hero-content">
            <span class="hero-tag-badge">{featured_art.get('category', 'Global Banking').upper()}</span>
            <div class="hero-headline">{featured_art.get('title')}</div>
            <div class="hero-byline">
                <span>By {featured_art.get('author') or 'James Sterling'}</span>
                <span>•</span>
                <span>{hero_date}</span>
                <span>•</span>
                <span>⏱️ {featured_art.get('read_time', '8 min read')}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_hero_click1, col_hero_click2 = st.columns([8, 2])
    with col_hero_click2:
        if st.button("Read Featured Analysis ›", use_container_width=True):
            st.session_state.active_article = featured_art
            st.session_state.view_mode = "article"
            st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Main 2-Column Editorial Grid (70% Left / 30% Right)
    col_insights_stream, col_sidebar_widgets = st.columns([68, 32])

    # LEFT COLUMN: LATEST INSIGHTS
    with col_insights_stream:
        st.markdown("""
        <div class="insights-header-row">
            <div class="insights-title">Latest Insights</div>
            <div class="sort-toggle-pill">
                <span class="sort-tab active">Most Recent</span>
                <span class="sort-tab">Recommended</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Show remaining articles as horizontal rows
        feed_articles = filtered_articles[1:] if len(filtered_articles) > 1 else filtered_articles

        if not feed_articles:
            st.markdown("""
            <div style="background: white; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 40px; text-align: center;">
                <div style="font-weight: 700; color: #0F172A; font-size: 16px;">No articles found matching criteria</div>
                <div style="color: #64748B; font-size: 13px; margin-top: 6px;">Try adjusting your search query or selecting ALL INSIGHTS above.</div>
            </div>
            """, unsafe_allow_html=True)

        for art in feed_articles:
            cat = art.get("category", "Regulation")
            tag_class = CATEGORIES.get(cat, {}).get("tag_class", "badge-tag-regulation")
            pub_date = format_display_date(art.get("publishedAt"))

            col_entry_card, col_entry_action = st.columns([85, 15])
            with col_entry_card:
                st.markdown(f"""
                <div class="insight-row-card">
                    <img src="{art.get('image_url')}" class="insight-thumbnail" alt="thumbnail" />
                    <div class="insight-body">
                        <div>
                            <div class="insight-meta-top">
                                <span class="{tag_class}">{cat.upper()}</span>
                                <span class="insight-date">📅 {pub_date} &nbsp;•&nbsp; ⏱️ {art.get('read_time', '6 min read')}</span>
                            </div>
                            <div class="insight-headline">{art['title']}</div>
                            <div class="insight-snippet">{art['description']}</div>
                        </div>
                        <div class="insight-footer-meta">
                            <span>Source: <b>{art.get('source')}</b></span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_entry_action:
                st.markdown("<div style='height: 38px;'></div>", unsafe_allow_html=True)
                if st.button("Read", key=f"read_btn_{art.get('id')}", use_container_width=True):
                    st.session_state.active_article = art
                    st.session_state.view_mode = "article"
                    st.rerun()

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        if st.button("Load More Professional Insights", use_container_width=True):
            st.toast("Displaying comprehensive global banking audit telemetry catalog.")

    # RIGHT COLUMN: INSTITUTIONAL WIDGETS
    with col_sidebar_widgets:
        # 1. DAILY LEADER WIDGET
        st.markdown("""
        <div class="sidebar-widget-box">
            <div class="widget-header-title">👤 DAILY LEADER</div>
            <div class="daily-leader-row">
                <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80" class="leader-avatar" alt="Elena Vance" />
                <div>
                    <div class="leader-name">Elena Vance</div>
                    <div class="leader-role">Chief Risk Officer</div>
                    <div class="leader-org">Global Banking Forum</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. TRENDING TOPICS WIDGET
        st.markdown("""
        <div class="sidebar-widget-box">
            <div class="widget-header-title">📈 TRENDING TOPICS</div>
            <div class="trending-item-row">
                <span class="trending-topic-title">Basel III Implementation</span>
                <span class="trending-count-pill">124</span>
            </div>
            <div class="trending-item-row">
                <span class="trending-topic-title">AI in Internal Audit</span>
                <span class="trending-count-pill">98</span>
            </div>
            <div class="trending-item-row">
                <span class="trending-topic-title">ESG Regulatory Updates</span>
                <span class="trending-count-pill">87</span>
            </div>
            <div class="trending-item-row">
                <span class="trending-topic-title">Cyber Resilience Frameworks</span>
                <span class="trending-count-pill">65</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. ACTIVE FILTERS WIDGET
        active_cat_label = st.session_state.selected_category if st.session_state.selected_category != "ALL INSIGHTS" else "Regulation"
        st.markdown(f"""
        <div class="sidebar-widget-box">
            <div class="widget-header-title">⛛ ACTIVE FILTERS</div>
            <div class="filter-item-row">
                <span class="filter-label">Classification</span>
                <span class="filter-val">{active_cat_label.title()}</span>
            </div>
            <div class="filter-item-row">
                <span class="filter-label">Date Range</span>
                <span class="filter-val">Last 7 Days</span>
            </div>
            <div class="filter-item-row">
                <span class="filter-label">Region</span>
                <span class="filter-val">Global</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. MARKET PULSE WIDGET
        st.markdown("""
        <div class="sidebar-widget-box">
            <div class="widget-header-title">↗ MARKET PULSE</div>
            <div class="market-ticker-row">
                <span class="ticker-symbol">SOFR 30D</span>
                <span class="ticker-figure">5.32% <span class="ticker-positive">+0.02%</span></span>
            </div>
            <div class="market-ticker-row">
                <span class="ticker-symbol">EURIBOR 3M</span>
                <span class="ticker-figure">3.98% <span class="ticker-negative">-0.05%</span></span>
            </div>
            <div class="market-ticker-row">
                <span class="ticker-symbol">BTC/USD</span>
                <span class="ticker-figure">34,124 <span class="ticker-positive">+1.42%</span></span>
            </div>
            <a href="#" class="terminal-link">View Terminal Data ›</a>
        </div>
        """, unsafe_allow_html=True)

        # 5. AUDIT INTELLIGENCE BRIEF (SIGNATURE ROYAL BLUE NEWSLETTER)
        st.markdown("""
        <div class="newsletter-royal-card">
            <div class="newsletter-title">Audit Intelligence Brief</div>
            <div class="newsletter-copy">
                Receive critical regulatory updates and financial insights directly in your inbox daily.
            </div>
        </div>
        """, unsafe_allow_html=True)

        email_input = st.text_input("Work Email Address", placeholder="name@company.com", label_visibility="collapsed")
        if st.button("SUBSCRIBE", use_container_width=True):
            if "@" in email_input:
                st.success("Subscribed to the Audit Intelligence Briefing.")
            else:
                st.error("Please enter a valid business email.")


# ---------------------------------------------------------
# 13. FOOTER (EXACT MATCH TO VISILY DESIGN)
# ---------------------------------------------------------

st.markdown("""
<footer class="editorial-footer">
    <div class="footer-top-row">
        <div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 24px; height: 24px; background: #1D4ED8; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-size: 13px;">🛡️</div>
                <span style="font-weight: 800; font-size: 17px; color: #0F172A;">Audit Intel</span>
            </div>
            <div class="footer-brand-summary">
                The authoritative news and analysis platform for modern banking and audit professionals.
            </div>
        </div>
        <div class="footer-links-group">
            <a href="#" class="footer-link">About Us</a>
            <a href="#" class="footer-link">Contact</a>
            <a href="#" class="footer-link">Privacy Policy</a>
            <a href="#" class="footer-link">Terms of Service</a>
            <a href="#" class="footer-link">Ad Choices</a>
        </div>
    </div>
    <div class="footer-bottom-row">
        <span>© 2023 AUDIT INTEL MEDIA GROUP. ALL RIGHTS RESERVED.</span>
        <span>MARKET DATA PROVIDED BY FINANCIAL SYSTEMS CORP</span>
    </div>
</footer>
""", unsafe_allow_html=True)
