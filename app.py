import os
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
# 1. APPLICATION SETUP & APEX FUTURISTIC COMMAND CENTER CSS
# ---------------------------------------------------------

st.set_page_config(
    page_title="APEX | Executive Banking Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# World-class Futuristic Executive Theme: Deep space obsidian canvas, glassmorphism, cyan micro-glows, crystal contrast
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Dark Canvas */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0F172A 0%, #080C16 65%, #050811 100%);
        color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Streamlit Global Text Overrides */
    p, span, label, div {
        color: #E2E8F0;
    }

    /* Sidebar - Sleek Glassmorphism */
    [data-testid="stSidebar"] {
        background-color: #0B1120 !important;
        border-right: 1px solid rgba(56, 189, 248, 0.12) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4);
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* Sidebar Labels */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label p {
        color: #94A3B8 !important;
        font-size: 11.5px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Sliders - High-Tech Cyan Neon Track */
    [data-testid="stSlider"] div[data-testid="stThumbValue"],
    [data-testid="stSlider"] span {
        color: #38BDF8 !important;
        font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #38BDF8 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 12px #38BDF8 !important;
    }

    /* MultiSelect Container & Chips */
    [data-baseweb="select"] > div {
        background-color: #111C33 !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        border-radius: 12px !important;
    }
    [data-baseweb="tag"] {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.18), rgba(14, 165, 233, 0.1)) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 8px !important;
        padding: 3px 8px !important;
    }
    [data-baseweb="tag"] span {
        color: #38BDF8 !important;
        font-weight: 600 !important;
        font-size: 12px !important;
    }
    [data-baseweb="tag"] svg {
        fill: #38BDF8 !important;
    }

    /* Futuristic HUD Header */
    .hud-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(11, 17, 32, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 36px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
    }
    .hud-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, #38BDF8, #818CF8, transparent);
    }
    .hud-sub-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #38BDF8;
        display: flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .radar-pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 12px #10B981, 0 0 20px #10B981;
        animation: pulseAnimation 2s infinite ease-in-out;
    }
    @keyframes pulseAnimation {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.6; }
    }
    .hud-title {
        font-size: 32px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.8px;
        line-height: 1.2;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
    }
    .hud-live-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }
    .hud-desc {
        font-size: 14.5px;
        color: #94A3B8;
        max-width: 850px;
        line-height: 1.55;
    }

    /* Metric Telemetry Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(17, 25, 45, 0.7), rgba(11, 16, 30, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 10px 25px -8px rgba(56, 189, 248, 0.2);
    }
    .metric-card::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: rgba(56, 189, 248, 0.2);
    }
    .metric-label-mono {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px;
        font-weight: 700;
        color: #64748B;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .metric-value-display {
        font-size: 30px;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.5px;
        display: flex;
        align-items: baseline;
        gap: 6px;
    }
    .metric-sub {
        font-size: 11px;
        color: #38BDF8;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Pill-style Filter Tabs */
    div[data-testid="stTabs"] {
        margin-top: 14px;
        margin-bottom: 24px;
    }
    div[data-testid="stTabs"] [role="tablist"] {
        gap: 12px;
        border-bottom: none !important;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        border-radius: 30px !important;
        padding: 8px 22px !important;
        font-size: 13.5px !important;
        font-weight: 700 !important;
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #94A3B8 !important;
        transition: all 0.2s ease !important;
        backdrop-filter: blur(8px) !important;
    }
    div[data-testid="stTabs"] button[role="tab"] p,
    div[data-testid="stTabs"] button[role="tab"] span {
        color: #94A3B8 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stTabs"] button[role="tab"]:hover {
        border-color: rgba(56, 189, 248, 0.4) !important;
        color: #F8FAFC !important;
        background-color: rgba(56, 189, 248, 0.1) !important;
    }
    div[data-testid="stTabs"] button[role="tab"]:hover p {
        color: #38BDF8 !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(14, 165, 233, 0.12)) !important;
        border: 1px solid #38BDF8 !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.3) !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p,
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] span {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Dossier Intelligence Cards */
    .dossier-card {
        background: linear-gradient(145deg, rgba(16, 24, 43, 0.8) 0%, rgba(10, 16, 30, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }
    .dossier-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 14px 34px -8px rgba(56, 189, 248, 0.18);
        background: linear-gradient(145deg, rgba(20, 30, 54, 0.85) 0%, rgba(13, 20, 38, 0.95) 100%);
    }
    .card-meta-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
        flex-wrap: wrap;
        gap: 10px;
    }
    .source-identity {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .source-emblem {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
    }
    .source-name-text {
        font-size: 13.5px;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.2px;
    }
    .source-timestamp {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #64748B;
        font-weight: 500;
    }

    /* Relevance HUD Badge */
    .relevance-hud {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .relevance-pill {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .score-urgent {
        background: rgba(244, 63, 94, 0.15);
        border: 1px solid rgba(244, 63, 94, 0.35);
        color: #FB7185;
    }
    .score-elevated {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.35);
        color: #FBBF24;
    }
    .score-standard {
        background: rgba(56, 189, 248, 0.12);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38BDF8;
    }

    /* Category Tag */
    .category-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #94A3B8;
    }

    /* Card Headline */
    .card-headline {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.4;
        letter-spacing: -0.3px;
        margin-bottom: 12px;
    }

    /* Natural, High-Legibility Executive Summary */
    .card-narrative {
        font-size: 16px;
        font-weight: 400;
        color: #CBD5E1;
        line-height: 1.68;
        margin-bottom: 18px;
    }

    /* Detected Audit Control Tags */
    .risk-factors-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 16px;
    }
    .tag-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 4px;
        padding: 2px 7px;
    }

    /* Card Footer & Action Link */
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 14px;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    .action-link-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        font-weight: 600;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 7px 16px;
        border-radius: 8px;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    .action-link-btn:hover {
        background: #38BDF8;
        color: #080C16 !important;
        border-color: #38BDF8;
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.4);
        text-decoration: none;
    }

    /* Search Input Styling */
    .stTextInput>div>div>input {
        background-color: #0F172A !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 14px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.25) !important;
    }
    .stTextInput>div>div>input::placeholder {
        color: #64748B !important;
    }

    /* Primary Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0284C7, #0369A1) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 13.5px !important;
        padding: 10px 22px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.25) !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #38BDF8, #0284C7) !important;
        color: #080C16 !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. CORE INSTITUTIONAL BANKING INTELLIGENCE CONFIG
# ---------------------------------------------------------

CATEGORIES = {
    "Transformation": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance") AND ("digital transformation" OR "modernization" OR "core banking" OR "automation" OR "artificial intelligence" OR "generative AI" OR "cloud")',
        "icon": "⚡"
    },
    "Regulation": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "compliance" OR "risk" OR "governance") AND ("regulation" OR "regulatory" OR "supervision" OR "RBI" OR "Basel" OR "AML" OR "KYC" OR "sanctions" OR "prudential" OR "enforcement")',
        "icon": "⚖️"
    },
    "People": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "risk" OR "governance" OR "controls") AND ("appointed" OR "appointment" OR "CEO" OR "CFO" OR "CRO" OR "CISO" OR "chief audit" OR "internal audit" OR "audit committee" OR "board")',
        "icon": "👤"
    },
    "Global Banks": {
        "query": '("bank" OR "banking group" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance" OR "regulatory") AND ("HSBC" OR "JPMorgan" OR "JPMorgan Chase" OR "Citi" OR "Citigroup" OR "Barclays" OR "Deutsche Bank" OR "UBS" OR "BNP Paribas" OR "Santander" OR "Standard Chartered" OR "Bank of America" OR "Goldman Sachs" OR "Morgan Stanley" OR "Wells Fargo" OR "ING" OR "ICBC" OR "MUFG" OR "Mizuho")',
        "icon": "🌐"
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
    "Global Banks": [
        "hsbc", "jpmorgan", "jpmorgan chase", "citi", "citigroup", "barclays",
        "deutsche bank", "ubs", "bnpparibas", "bnp paribas", "santander",
        "standard chartered", "bank of america", "goldman sachs", "morgan stanley",
        "wells fargo", "ing", "icbc", "mufg", "mizuho",
    ],
}


# ---------------------------------------------------------
# 3. EXTRACTION LOGIC & SCORING FUNCTIONS
# ---------------------------------------------------------

def get_api_key():
    """Extract NewsAPI key from config, env, or secrets."""
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
    """Fast, transparent audit relevance scoring (0-100)."""
    score = 0
    for term in AUDIT_TERMS:
        if term in text:
            score += 6

    # Stronger signals get additional weight
    for term in [
        "internal audit", "audit committee", "internal controls",
        "control deficiency", "regulatory enforcement",
        "model risk", "financial crime", "basel",
    ]:
        if term in text:
            score += 12

    return min(score, 100)


def extract_matched_tags(text):
    """Extract key detected audit/governance topics as tags."""
    matched = []
    key_topics = [
        ("Internal Controls", "Internal-Controls"),
        ("Audit Committee", "Audit-Committee"),
        ("Model Risk", "Model-Risk"),
        ("Basel", "Basel-Prudential"),
        ("AML", "AML/KYC"),
        ("Compliance", "Compliance"),
        ("Core Banking", "Core-Banking"),
        ("Digital Transformation", "Transformation"),
        ("Regulatory Enforcement", "Enforcement"),
        ("Governance", "Governance"),
    ]
    for phrase, tag in key_topics:
        if phrase.lower() in text:
            matched.append(tag)
        if len(matched) >= 3:
            break
    if not matched:
        matched.append("Banking-Audit")
    return matched


def classify_article(article):
    """Classify using keyword matching."""
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
    """Fetch targeted stream from NewsAPI."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": api_key,
    }

    response = requests.get(url, params=params, timeout=20)
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
def load_news(api_key, lookback_days, page_size):
    """
    Fetch all 4 targeted banking categories concurrently.
    Cached for 5 minutes.
    """
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

    # Deduplicate by URL and normalized title
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

    cleaned = []
    for article in unique.values():
        text = normalize_text(article)
        relevance = audit_relevance(text)

        if relevance < 5:
            continue

        category, category_score = classify_article(article)
        matched_tags = extract_matched_tags(text)

        source = article.get("source") or {}
        published = article.get("publishedAt") or ""

        cleaned.append({
            "category": category,
            "audit_relevance": relevance,
            "category_score": category_score,
            "title": article.get("title") or "Untitled Intelligence Record",
            "description": article.get("description") or "",
            "source": source.get("name") or "Institutional Source",
            "publishedAt": published,
            "url": article.get("url") or "",
            "tags": matched_tags,
        })

    cleaned.sort(key=lambda x: (x["audit_relevance"], x["publishedAt"]), reverse=True)
    return cleaned, errors


def format_relative_time(pub_date_str):
    """Format timestamps into clean relative format."""
    if not pub_date_str:
        return "Recent"
    try:
        clean_str = pub_date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_str)
        now = datetime.now(timezone.utc)
        diff = now - dt
        days = diff.days
        if days == 0:
            return "Today"
        elif days == 1:
            return "1d ago"
        elif days < 7:
            return f"{days}d ago"
        elif days < 14:
            return "1w ago"
        else:
            return f"{days // 7}w ago"
    except Exception:
        return pub_date_str[:10] if len(pub_date_str) >= 10 else "Recent"


# ---------------------------------------------------------
# 4. SIDEBAR: FUTURISTIC COMMAND PANEL
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="padding: 6px 0 16px 0; border-bottom: 1px solid rgba(56, 189, 248, 0.15); margin-bottom: 18px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 38px; height: 38px; border-radius: 10px; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.35); display: flex; align-items: center; justify-content: center; font-size: 18px; box-shadow: 0 0 14px rgba(56, 189, 248, 0.2);">
                🏛️
            </div>
            <div>
                <div style="font-size: 16px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.3px;">APEX INTELLIGENCE</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #38BDF8; font-weight: 700; letter-spacing: 0.6px; text-transform: uppercase;">BANKING AUDIT TELEMETRY</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_key = get_api_key()

    if not api_key:
        api_key = st.text_input(
            "NEWSAPI CREDENTIALS",
            type="password",
            placeholder="Enter API key...",
            help="Configure API_KEY in Streamlit secrets or supply temporary key.",
        )

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

    lookback_days = st.slider(
        "Lookback Window (Days)",
        min_value=1,
        max_value=7,
        value=3,
    )

    page_size = st.slider(
        "Ingestion Depth (Per Stream)",
        min_value=10,
        max_value=100,
        value=50,
        step=10,
    )

    selected_categories = st.multiselect(
        "Surveillance Sectors",
        options=list(CATEGORIES.keys()),
        default=list(CATEGORIES.keys()),
    )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    refresh = st.button("Initiate Radar Sweep", use_container_width=True)

    st.markdown("""
    <div style="margin-top: 24px; padding: 14px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; font-size: 11.5px; color: #94A3B8; line-height: 1.6;">
        <div style="font-family: 'JetBrains Mono', monospace; color: #38BDF8; font-weight: 700; margin-bottom: 4px; text-transform: uppercase;">Supervisory Scope</div>
        Continuous tracking across Basel III/IV Prudential Standards, RBI Circulars, SOX 404 Internal Controls, Executive Appointments, and Global SIFI Banks.
    </div>
    """, unsafe_allow_html=True)

if not api_key:
    st.info("⚡ Please enter your NewsAPI key in the sidebar command panel or configure it in Streamlit secrets.")
    st.stop()


# ---------------------------------------------------------
# 5. DATA INGESTION & FILTERING
# ---------------------------------------------------------

if refresh or "news_loaded" not in st.session_state:
    with st.spinner("Synchronizing institutional banking surveillance telemetry..."):
        articles, errors = load_news(api_key, lookback_days, page_size)

    st.session_state.news = articles
    st.session_state.news_errors = errors
    st.session_state.news_loaded = True

articles = st.session_state.get("news", [])
errors = st.session_state.get("news_errors", [])

if selected_categories:
    filtered = [a for a in articles if a["category"] in selected_categories]
else:
    filtered = []


# ---------------------------------------------------------
# 6. EXECUTIVE HUD HEADER & TELEMETRY STRIP
# ---------------------------------------------------------

st.markdown(f"""
<div class="hud-header">
    <div class="hud-sub-badge">
        <span class="radar-pulse-dot"></span>
        <span>GLOBAL BANKING AUDIT INTELLIGENCE &nbsp;//&nbsp; CONTINUOUS TELEMETRY</span>
    </div>
    <div class="hud-title">
        <span>Institutional Risk & Assurance Radar</span>
        <span class="hud-live-tag">LIVE HUD</span>
    </div>
    <div class="hud-desc">
        Real-time strategic surveillance engine curated for Board Audit Committees, Chief Risk Officers, and Senior Regulatory Assurance Leaders.
    </div>
</div>
""", unsafe_allow_html=True)

# HUD Metrics Flight Deck
m1, m2, m3, m4, m5 = st.columns(5)
total_count = len(filtered)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label-mono">TOTAL SIGNALS</div>
        <div class="metric-value-display">
            <span>{total_count}</span>
            <span class="metric-sub">ACT</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    trans_count = sum(a["category"] == "Transformation" for a in filtered)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label-mono" style="color: #38BDF8;">TRANSFORMATION</div>
        <div class="metric-value-display">
            <span>{trans_count}</span>
            <span class="metric-sub">CORE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    reg_count = sum(a["category"] == "Regulation" for a in filtered)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label-mono" style="color: #FBBF24;">REGULATION</div>
        <div class="metric-value-display">
            <span>{reg_count}</span>
            <span class="metric-sub">BASEL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    people_count = sum(a["category"] == "People" for a in filtered)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label-mono" style="color: #A78BFA;">PEOPLE / BOARD</div>
        <div class="metric-value-display">
            <span>{people_count}</span>
            <span class="metric-sub">LEAD</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    global_count = sum(a["category"] == "Global Banks" for a in filtered)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label-mono" style="color: #34D399;">GLOBAL SIFIs</div>
        <div class="metric-value-display">
            <span>{global_count}</span>
            <span class="metric-sub">TIER-1</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

if errors:
    with st.expander("Telemetry Diagnostic Alerts", expanded=False):
        for err in errors:
            st.markdown(f"<div style='font-family: monospace; font-size: 12px; color: #FBBF24;'>[NOTICE] {err}</div>", unsafe_allow_html=True)

# Instant Search Bar
search_query = st.text_input(
    "Filter Intelligence Telemetry",
    placeholder="Search telemetry by bank (JPMorgan, HSBC), regulator (RBI, Basel, ECB), or control deficiency...",
    label_visibility="collapsed"
)

if search_query:
    sq = search_query.lower()
    filtered = [
        a for a in filtered
        if sq in a["title"].lower() or sq in a["description"].lower() or sq in a["source"].lower()
    ]


# ---------------------------------------------------------
# 7. HIGH-TECH TABS & INTELLIGENCE DOSSIER CARDS
# ---------------------------------------------------------

if not filtered:
    st.markdown("""
    <div style="text-align: center; padding: 50px; background: rgba(15, 23, 42, 0.6); border-radius: 16px; border: 1px dashed rgba(56, 189, 248, 0.2); margin-top: 14px;">
        <div style="font-size: 18px; font-weight: 700; color: #F8FAFC;">No telemetry records matching criteria</div>
        <div style="font-size: 13.5px; color: #94A3B8; margin-top: 6px;">Adjust search keywords or expand lookback days in the sidebar command panel.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    tabs = st.tabs(["All Telemetry"] + [f"{c}" for c in selected_categories])

    def render_dossier_stream(rows):
        for art in rows:
            cat = art["category"]
            cat_icon = CATEGORIES.get(cat, {}).get("icon", "🏛️")
            rel_time = format_relative_time(art["publishedAt"])
            score = art["audit_relevance"]

            # HUD Score styling
            if score >= 75:
                score_class = "score-urgent"
                score_label = "CRITICAL FINDING"
            elif score >= 50:
                score_class = "score-elevated"
                score_label = "ELEVATED WATCH"
            else:
                score_class = "score-standard"
                score_label = "STANDARD ASSURANCE"

            description_text = art["description"] if art["description"] else "No extended abstract provided by source dispatch. Access verified primary source below."

            tags_html = "".join([f'<span class="tag-chip">#{tag}</span>' for tag in art.get("tags", [])])

            st.markdown(f"""
            <div class="dossier-card">
                <div class="card-meta-bar">
                    <div class="source-identity">
                        <div class="source-emblem">{cat_icon}</div>
                        <div>
                            <span class="source-name-text">{art['source']}</span>
                            <span style="color: #475569; margin: 0 6px;">•</span>
                            <span class="source-timestamp">{rel_time}</span>
                        </div>
                    </div>
                    <div class="relevance-hud">
                        <span class="category-chip">{cat}</span>
                        <span class="relevance-pill {score_class}">
                            <span>●</span>
                            <span>{score_label} &nbsp;{score}/100</span>
                        </span>
                    </div>
                </div>
                <div class="card-headline">
                    {art['title']}
                </div>
                <div class="card-narrative">
                    {description_text}
                </div>
                <div class="risk-factors-row">
                    {tags_html}
                </div>
                <div class="card-footer">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #64748B;">
                        STATUS: VERIFIED TELEMETRY
                    </div>
                    <div>
                        <a href="{art['url']}" target="_blank" class="action-link-btn">
                            <span>Inspect Source Dossier</span>
                            <span style="font-size: 14px;">↗</span>
                        </a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[0]:
        render_dossier_stream(filtered)

    for tab, category in zip(tabs[1:], selected_categories):
        with tab:
            cat_rows = [a for a in filtered if a["category"] == category]
            if not cat_rows:
                st.markdown(f"""
                <div style="text-align: center; padding: 36px; background: rgba(15, 23, 42, 0.6); border-radius: 14px; border: 1px dashed rgba(255, 255, 255, 0.08);">
                    <div style="font-size: 14px; color: #94A3B8;">No records logged under {category}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                render_dossier_stream(cat_rows)


# ---------------------------------------------------------
# 8. EXECUTIVE EXPORT & FOOTER
# ---------------------------------------------------------
st.markdown("<hr style='margin-top: 36px; border-color: rgba(255, 255, 255, 0.08);' />", unsafe_allow_html=True)
col_down1, col_down2 = st.columns([8, 2])
with col_down1:
    st.markdown("""
    <div style="font-size: 12px; color: #64748B; font-family: 'JetBrains Mono', monospace;">
        APEX BANKING INTELLIGENCE RADAR • CONFIDENTIAL EXECUTIVE TELEMETRY FOR INTERNAL AUDIT & RISK COMMITTEES
    </div>
    """, unsafe_allow_html=True)
with col_down2:
    if filtered:
        df_export = pd.DataFrame(filtered)
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Dossier (CSV)",
            data=csv,
            file_name=f"banking_audit_dossier_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
