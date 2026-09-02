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
# 1. APP CONFIGURATION & SLEEK EXECUTIVE FUTURISTIC THEME
# ---------------------------------------------------------

st.set_page_config(
    page_title="Audit Intelligence | Executive Banking Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Refined, High-End Executive Theme: Clean, minimal palette, natural typography, spacious reading font
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Body Font and Background */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {
        background-color: #0F1626;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.08);
    }

    /* Top Brand Nav */
    .brand-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 0 16px 0;
        margin-bottom: 8px;
    }
    .brand-logo-badge {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #1E293B, #0F172A);
        border: 1px solid rgba(56, 189, 248, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35);
    }
    .brand-title {
        font-size: 15px;
        font-weight: 700;
        letter-spacing: -0.2px;
        color: #F8FAFC;
    }
    .brand-subtitle {
        font-size: 11px;
        font-weight: 500;
        color: #38BDF8;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* Futuristic Executive Header */
    .executive-header {
        background: radial-gradient(ellipse at top left, #141E33 0%, #0F172A 50%, #0B0F19 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    .executive-header::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.3), transparent);
    }
    .exec-headline {
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .exec-badge {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.6px;
        padding: 3px 10px;
        border-radius: 20px;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #38BDF8;
        text-transform: uppercase;
    }
    .exec-desc {
        font-size: 14.5px;
        color: #94A3B8;
        line-height: 1.5;
        max-width: 820px;
        font-weight: 400;
    }
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        font-weight: 600;
        color: #34D399;
    }
    .live-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Professional Metric Cards */
    .metric-card {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
    }
    .metric-label {
        font-size: 11.5px;
        font-weight: 600;
        color: #94A3B8;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .metric-val {
        font-size: 26px;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.5px;
    }

    /* Article Card - Natural, High Legibility */
    .article-container {
        background: #101626;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 18px;
        transition: all 0.2s ease-in-out;
    }
    .article-container:hover {
        border-color: rgba(56, 189, 248, 0.35);
        background: #131A2E;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    .article-meta-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        flex-wrap: wrap;
        gap: 8px;
    }
    .category-tag {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.4px;
        padding: 4px 10px;
        border-radius: 6px;
        background: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.25);
    }
    .score-badge {
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace;
    }
    .score-high {
        background: rgba(244, 63, 94, 0.12);
        border: 1px solid rgba(244, 63, 94, 0.3);
        color: #FB7185;
    }
    .score-mid {
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #FBBF24;
    }
    .score-std {
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #38BDF8;
    }
    .article-date {
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
    }

    .article-title-text {
        font-size: 18px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.45;
        letter-spacing: -0.2px;
        margin-bottom: 10px;
    }

    /* Increased Summary Font Size - Natural, Readable & Non-robotic */
    .article-summary-text {
        font-size: 15px;
        font-weight: 400;
        color: #CBD5E1;
        line-height: 1.65;
        margin-bottom: 18px;
    }

    /* Minimal Elegant Button */
    .read-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12.5px;
        font-weight: 600;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 7px 14px;
        border-radius: 8px;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    .read-btn:hover {
        background: #38BDF8;
        color: #0B0F19;
        border-color: #38BDF8;
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25);
    }

    /* Custom Streamlit Input Overrides */
    .stTextInput>div>div>input {
        background-color: #101626 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #F8FAFC !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 0 1px #38BDF8 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0284C7, #0369A1);
        color: white;
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 10px;
        font-weight: 600;
        font-size: 13.5px;
        padding: 8px 18px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #38BDF8, #0284C7);
        color: #0B0F19;
        border-color: #38BDF8;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. EXACT EXTRACTION CATEGORIES & QUERIES
# ---------------------------------------------------------

CATEGORIES = {
    "Transformation": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance") AND ("digital transformation" OR "modernization" OR "core banking" OR "automation" OR "artificial intelligence" OR "generative AI" OR "cloud")'
    },
    "Regulation": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "compliance" OR "risk" OR "governance") AND ("regulation" OR "regulatory" OR "supervision" OR "RBI" OR "Basel" OR "AML" OR "KYC" OR "sanctions" OR "prudential" OR "enforcement")'
    },
    "People": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "risk" OR "governance" OR "controls") AND ("appointed" OR "appointment" OR "CEO" OR "CFO" OR "CRO" OR "CISO" OR "chief audit" OR "internal audit" OR "audit committee" OR "board")'
    },
    "Cyber and Tech": {
        "query": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "IT controls" OR "risk" OR "governance") AND ("cybersecurity" OR "cyber attack" OR "ransomware" OR "data breach" OR "information security" OR "technology risk" OR "IT audit" OR "cloud security" OR "AI governance" OR "model risk")'
    },
    "Global Banks": {
        "query": '("bank" OR "banking group" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance" OR "regulatory") AND ("HSBC" OR "JPMorgan" OR "JPMorgan Chase" OR "Citi" OR "Citigroup" OR "Barclays" OR "Deutsche Bank" OR "UBS" OR "BNP Paribas" OR "Santander" OR "Standard Chartered" OR "Bank of America" OR "Goldman Sachs" OR "Morgan Stanley" OR "Wells Fargo" OR "ING" OR "ICBC" OR "MUFG" OR "Mizuho")'
    },
}

# Unified, harmonious color theme (Professional, minimal palette)
CATEGORY_COLORS = {
    "Transformation": "#38BDF8",
    "Regulation": "#FBBF24",
    "People": "#A78BFA",
    "Cyber and Tech": "#FB7185",
    "Global Banks": "#34D399"
}

AUDIT_TERMS = [
    "internal audit", "external audit", "audit committee", "auditor",
    "audit finding", "audit findings", "internal control", "internal controls",
    "control weakness", "control weaknesses", "control deficiency",
    "control deficiencies", "governance", "risk management", "operational risk",
    "model risk", "compliance", "regulatory", "regulation", "supervision",
    "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
    "sanctions", "cybersecurity", "cyber security", "it audit", "technology risk",
    "data breach", "ransomware", "fraud", "misconduct", "financial crime",
]

CATEGORY_TERMS = {
    "Transformation": [
        "digital transformation", "modernization", "modernisation", "core banking",
        "automation", "artificial intelligence", "generative ai", "genai",
        "machine learning", "cloud", "digital banking", "technology transformation",
        "operating model",
    ],
    "Regulation": [
        "regulation", "regulatory", "rbi", "basel", "prudential", "supervision",
        "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
        "sanctions", "capital requirements", "regulatory capital", "compliance",
    ],
    "People": [
        "appointed", "appointment", "ceo", "cfo", "cro", "ciso", "chief audit",
        "internal audit", "audit committee", "board", "director", "chairman",
        "chairwoman", "leadership", "executive",
    ],
    "Cyber and Tech": [
        "cybersecurity", "cyber security", "cyber attack", "ransomware",
        "data breach", "information security", "technology risk", "it audit",
        "cloud security", "ai governance", "model risk", "digital", "technology",
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
    """Use Streamlit secrets/env first; sidebar entry is the local fallback."""
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
    """Simple, fast, transparent audit relevance score: 0-100."""
    score = 0
    for term in AUDIT_TERMS:
        if term in text:
            score += 5

    # Stronger signals get additional weight.
    for term in [
        "internal audit", "audit committee", "internal controls",
        "control deficiency", "regulatory enforcement", "it audit",
        "technology risk", "financial crime",
    ]:
        if term in text:
            score += 10

    return min(score, 100)


def classify_article(article):
    """Classify using transparent keyword scoring; no paid LLM is required."""
    text = normalize_text(article)
    scores = {}

    for category, terms in CATEGORY_TERMS.items():
        score = 0
        for term in terms:
            if term in text:
                score += 1
        scores[category] = score

    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        best_category = "Regulation"

    return best_category, scores[best_category]


def fetch_category(category, query, api_key, from_date, page_size):
    """Fetch one category from NewsAPI."""
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
    Fetch all five targeted searches in parallel.
    Cached for 5 minutes so Streamlit reruns do not repeatedly call NewsAPI.
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

    # Deduplicate by URL first, then by normalized title.
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

        # Only retain stories with a meaningful audit/risk/control signal.
        if relevance < 5:
            continue

        category, category_score = classify_article(article)

        source = article.get("source") or {}
        published = article.get("publishedAt") or ""

        cleaned.append({
            "category": category,
            "audit_relevance": relevance,
            "category_score": category_score,
            "title": article.get("title") or "Untitled",
            "description": article.get("description") or "",
            "source": source.get("name") or "Unknown source",
            "publishedAt": published,
            "url": article.get("url") or "",
            "author": article.get("author") or "",
        })

    cleaned.sort(key=lambda x: (x["audit_relevance"], x["publishedAt"]), reverse=True)
    return cleaned, errors


# ---------------------------------------------------------
# 4. SIDEBAR: PROFESSIONAL CONTROLS
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div class="brand-header">
        <div class="brand-logo-badge">🏛️</div>
        <div>
            <div class="brand-title">Audit Intelligence</div>
            <div class="brand-subtitle">Banking Surveillance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_key = get_api_key()

    if not api_key:
        api_key = st.text_input(
            "NewsAPI Key",
            type="password",
            placeholder="Enter API key...",
            help="Your key is used only for this session, or configure API_KEY in secrets.toml.",
        )

    st.markdown("<hr style='margin: 14px 0;' />", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 11px; color: #94A3B8; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 10px; text-transform: uppercase;'>Filters & Controls</div>", unsafe_allow_html=True)

    lookback_days = st.slider(
        "Lookback Window (Days)",
        min_value=1,
        max_value=7,
        value=3,
    )

    page_size = st.slider(
        "Articles Per Stream",
        min_value=10,
        max_value=100,
        value=50,
        step=10,
    )

    selected_categories = st.multiselect(
        "Intelligence Categories",
        options=list(CATEGORIES.keys()),
        default=list(CATEGORIES.keys()),
    )

    min_relevance = st.slider(
        "Minimum Relevance Threshold",
        min_value=5,
        max_value=50,
        value=5,
        step=5,
    )

    high_priority_only = st.checkbox("High-Priority Only (Score ≥ 50)", value=False)

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    refresh = st.button("Refresh Surveillance", type="primary", use_container_width=True)

    st.markdown("<hr style='margin: 20px 0;' />", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 11.5px; color: #64748B; line-height: 1.5;">
        <b>Internal Controls Coverage:</b><br/>
        Real-time intelligence on Basel III/IV, RBI, ECB, SOX, AML/KYC, and Model Governance.
    </div>
    """, unsafe_allow_html=True)

if not api_key:
    st.warning("Please enter your NewsAPI key in the sidebar or configure API_KEY in Streamlit secrets.")
    st.stop()


# ---------------------------------------------------------
# 5. DATA INGESTION & FILTERING
# ---------------------------------------------------------

if refresh or "news_loaded" not in st.session_state:
    with st.spinner("Analyzing real-time institutional banking intelligence..."):
        articles, errors = load_news(api_key, lookback_days, page_size)

    st.session_state.news = articles
    st.session_state.news_errors = errors
    st.session_state.news_loaded = True

articles = st.session_state.get("news", [])
errors = st.session_state.get("news_errors", [])

if selected_categories:
    filtered = [
        a for a in articles
        if a["category"] in selected_categories
        and a["audit_relevance"] >= min_relevance
    ]
else:
    filtered = []

if high_priority_only:
    filtered = [a for a in filtered if a["audit_relevance"] >= 50]


# ---------------------------------------------------------
# 6. EXECUTIVE HEADER & METRICS
# ---------------------------------------------------------

st.markdown(f"""
<div class="executive-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; flex-wrap: wrap; gap: 12px;">
        <div class="exec-headline">
            <span>Global Banking Audit Intelligence</span>
            <span class="exec-badge">Executive Radar</span>
        </div>
        <div class="status-indicator">
            <span class="live-dot"></span>
            <span>Continuous Monitoring Active</span>
        </div>
    </div>
    <div class="exec-desc">
        Independent surveillance stream for Internal Audit, Board Risk Committees, and Regulatory Compliance Officers.
    </div>
</div>
""", unsafe_allow_html=True)

# Metrics Grid - Clean, Professional
c1, c2, c3, c4, c5 = st.columns(5)
total_streams = len(filtered)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Findings</div>
        <div class="metric-val">{total_streams}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #38BDF8;">Transformation</div>
        <div class="metric-val">{sum(a["category"] == "Transformation" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #FBBF24;">Regulation</div>
        <div class="metric-val">{sum(a["category"] == "Regulation" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #FB7185;">Cyber & Tech</div>
        <div class="metric-val">{sum(a["category"] == "Cyber and Tech" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label" style="color: #34D399;">Global Banks</div>
        <div class="metric-val">{sum(a["category"] == "Global Banks" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

if errors:
    with st.expander("Feed Alerts / Notices", expanded=False):
        for err in errors:
            st.markdown(f"<div style='font-size: 12px; color: #FBBF24;'>• {err}</div>", unsafe_allow_html=True)

# Search Input
search_query = st.text_input(
    "Search Intelligence",
    placeholder="Search by institution (JPMorgan, HSBC), regulator (RBI, Basel), or control topic...",
    label_visibility="collapsed"
)

if search_query:
    sq = search_query.lower()
    filtered = [
        a for a in filtered
        if sq in a["title"].lower() or sq in a["description"].lower() or sq in a["source"].lower()
    ]


# ---------------------------------------------------------
# 7. NATURAL, HIGH-LEGIBILITY FEED
# ---------------------------------------------------------

if not filtered:
    st.markdown("""
    <div style="text-align: center; padding: 48px; background: #101626; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.12); margin-top: 14px;">
        <div style="font-size: 16px; font-weight: 600; color: #E2E8F0;">No signals match the current criteria</div>
        <div style="font-size: 13.5px; color: #64748B; margin-top: 6px;">Try adjusting your search query, increasing lookback days, or adjusting relevance filters in the sidebar.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    tabs = st.tabs(["All Intelligence"] + [f"{c}" for c in selected_categories])

    def render_articles(rows):
        for art in rows:
            cat = art["category"]
            cat_color = CATEGORY_COLORS.get(cat, "#38BDF8")
            score = art["audit_relevance"]

            if score >= 75:
                score_class = "score-high"
                score_label = "Priority Action"
            elif score >= 50:
                score_class = "score-mid"
                score_label = "Elevated Watch"
            else:
                score_class = "score-std"
                score_label = "Standard Signal"

            formatted_date = art["publishedAt"].replace("T", " ").replace("Z", "")[:16] if art["publishedAt"] else "Recent"

            description_text = art["description"] if art["description"] else "No expanded narrative provided by the news source. Click below to inspect the full coverage."

            st.markdown(f"""
            <div class="article-container">
                <div class="article-meta-row">
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span class="category-tag">
                            {cat}
                        </span>
                        <span class="score-badge {score_class}">
                            {score_label} &nbsp;{score}/100
                        </span>
                    </div>
                    <div class="article-date">
                        {art['source']} &nbsp;•&nbsp; {formatted_date}
                    </div>
                </div>
                <div class="article-title-text">
                    {art['title']}
                </div>
                <div class="article-summary-text">
                    {description_text}
                </div>
                <div style="display: flex; justify-content: flex-end; align-items: center;">
                    <a href="{art['url']}" target="_blank" class="read-btn">
                        <span>Read Full Report</span>
                        <span style="font-size: 14px;">↗</span>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[0]:
        render_articles(filtered)

    for tab, category in zip(tabs[1:], selected_categories):
        with tab:
            cat_rows = [a for a in filtered if a["category"] == category]
            if not cat_rows:
                st.markdown(f"""
                <div style="text-align: center; padding: 36px; background: #101626; border-radius: 12px; border: 1px dashed rgba(255, 255, 255, 0.08);">
                    <div style="font-size: 14px; color: #94A3B8;">No records found under {category}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                render_articles(cat_rows)

# ---------------------------------------------------------
# 8. EXPORT FOR COMMITTEES
# ---------------------------------------------------------
st.markdown("<hr style='margin-top: 36px; border-color: rgba(255, 255, 255, 0.07);' />", unsafe_allow_html=True)
col_down1, col_down2 = st.columns([8, 2])
with col_down1:
    st.markdown("""
    <div style="font-size: 12px; color: #64748B;">
        Institutional Banking Surveillance System • Export intelligence telemetry for Audit and Risk Committees
    </div>
    """, unsafe_allow_html=True)
with col_down2:
    if filtered:
        df_export = pd.DataFrame(filtered)
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV Report",
            data=csv,
            file_name=f"banking_audit_intel_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
