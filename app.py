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
# 1. APP CONFIGURATION & FUTURISTIC OBSIDIAN THEME
# ---------------------------------------------------------

st.set_page_config(
    page_title="AUDIT INTELLIGENCE // BANK TERMINAL",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyber-Obsidian Banking Terminal CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700;800&family=Inter:wght@300;400;600;700&display=swap');

    /* Global Theme Overrides */
    .stApp {
        background-color: #06090F;
        color: #F1F5F9;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0B101E;
        border-right: 1px solid rgba(0, 229, 255, 0.15);
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(0, 229, 255, 0.15);
    }

    /* Monospace Terminal Headers */
    h1, h2, h3, .terminal-mono {
        font-family: 'JetBrains Mono', monospace !important;
        letter-spacing: -0.5px;
    }

    /* Futuristic HUD Header */
    .hud-container {
        background: linear-gradient(135deg, #0B132B 0%, #0D1B3E 50%, #06090F 100%);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.08);
        position: relative;
        overflow: hidden;
    }
    .hud-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00E5FF, #38BDF8, #8B5CF6);
    }
    .hud-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hud-badge {
        background: rgba(0, 229, 255, 0.15);
        border: 1px solid rgba(0, 229, 255, 0.5);
        color: #00E5FF;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .live-pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
        animation: pulse 1.8s infinite;
        margin-right: 6px;
    }
    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }

    /* Metric Cards */
    .metric-card {
        background: #0D1424;
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        padding: 14px 18px;
        text-align: left;
    }
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #94A3B8;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 700;
        color: #FFFFFF;
    }

    /* Article Cards */
    .article-card {
        background-color: #0D1424;
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
        transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .article-card:hover {
        border-color: rgba(0, 229, 255, 0.5);
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.08);
    }
    .cat-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        letter-spacing: 0.5px;
        display: inline-block;
    }
    .score-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    .score-critical {
        background: rgba(244, 63, 94, 0.15);
        border: 1px solid rgba(244, 63, 94, 0.5);
        color: #F43F5E;
    }
    .score-elevated {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #F59E0B;
    }
    .score-monitor {
        background: rgba(0, 229, 255, 0.15);
        border: 1px solid rgba(0, 229, 255, 0.5);
        color: #00E5FF;
    }

    /* Form & Input Elements */
    .stTextInput>div>div>input {
        background-color: #0D1424 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0284C7, #0369A1);
        color: white;
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00E5FF, #0284C7);
        color: #06090F;
        border-color: #00E5FF;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
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

CATEGORY_COLORS = {
    "Transformation": "#00E5FF",
    "Regulation": "#F59E0B",
    "People": "#8B5CF6",
    "Cyber and Tech": "#F43F5E",
    "Global Banks": "#10B981"
}

# Extra audit vocabulary is used to remove ordinary banking stories.
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
# 4. SIDEBAR: CONTROLS & SECURITY PARAMETERS
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <span style="font-size: 24px;">🛡️</span>
        <div>
            <div style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 14px; color: #FFFFFF;">AEGIS TERMINAL</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 9px; color: #00E5FF;">BANK RISK TELEMETRY</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_key = get_api_key()

    if not api_key:
        api_key = st.text_input(
            "NEWSAPI_KEY CREDENTIAL",
            type="password",
            help="Your key is used only for this Streamlit session, or configure API_KEY in secrets.toml.",
        )

    st.markdown("<hr style='margin: 15px 0;' />", unsafe_allow_html=True)
    st.markdown("<div class='terminal-mono' style='font-size: 11px; color: #94A3B8; font-weight: 700; margin-bottom: 8px;'>SCANNER CONTROLS</div>", unsafe_allow_html=True)

    lookback_days = st.slider(
        "Lookback Window (Days)",
        min_value=1,
        max_value=7,
        value=3,
    )

    page_size = st.slider(
        "Articles Per Category",
        min_value=10,
        max_value=100,
        value=50,
        step=10,
    )

    selected_categories = st.multiselect(
        "Active Intelligence Streams",
        options=list(CATEGORIES.keys()),
        default=list(CATEGORIES.keys()),
    )

    min_relevance = st.slider(
        "Min Audit Relevance Threshold",
        min_value=5,
        max_value=50,
        value=5,
        step=5,
    )

    high_priority_only = st.checkbox("⚡ High-Priority Alerts Only (Score ≥ 50)", value=False)

    refresh = st.button("RUN REGULATORY SCAN", type="primary", use_container_width=True)

    st.markdown("<hr style='margin: 20px 0;' />", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family: 'JetBrains Mono'; font-size: 9px; color: #64748B; line-height: 1.4;">
        <b>ZERO-TRUST COMPLIANCE NOTICE:</b><br/>
        Surveillance streams utilize weighted domain vocabulary (Basel, RBI, ECB, SOX, AML, Model Risk).
    </div>
    """, unsafe_allow_html=True)

if not api_key:
    st.warning("⚠️ Enter your NewsAPI key in the sidebar or configure API_KEY in Streamlit secrets.")
    st.stop()


# ---------------------------------------------------------
# 5. DATA INGESTION & FILTERING
# ---------------------------------------------------------

if refresh or "news_loaded" not in st.session_state:
    with st.spinner("Executing real-time multi-threaded banking intelligence scan..."):
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
# 6. FUTURISTIC HUD HEADER & KPI METRICS
# ---------------------------------------------------------

st.markdown(f"""
<div class="hud-container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div class="hud-title">
            <span>AUDIT INTELLIGENCE</span>
            <span class="hud-badge">BANK // OS v2.8</span>
        </div>
        <div style="font-family: 'JetBrains Mono'; font-size: 11px; color: #94A3B8;">
            <span class="live-pulse"></span>INSTITUTIONAL RISK RADAR // LIVE
        </div>
    </div>
    <div style="font-size: 13px; color: #94A3B8; max-width: 800px;">
        Real-time global banking surveillance for Internal Audit, Risk Committees, Control Officers, and Supervisory Compliance.
    </div>
</div>
""", unsafe_allow_html=True)

# KPI Metrics Row
c1, c2, c3, c4, c5 = st.columns(5)
total_streams = len(filtered)
critical_alerts = sum(1 for a in filtered if a["audit_relevance"] >= 75)
elevated_alerts = sum(1 for a in filtered if 50 <= a["audit_relevance"] < 75)
avg_score = int(sum(a["audit_relevance"] for a in filtered) / total_streams) if total_streams > 0 else 0

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TOTAL STORIES</div>
        <div class="metric-value">{total_streams}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="border-color: rgba(0, 229, 255, 0.4);">
        <div class="metric-label" style="color: #00E5FF;">TRANSFORMATION</div>
        <div class="metric-value" style="color: #00E5FF;">{sum(a["category"] == "Transformation" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="border-color: rgba(245, 158, 11, 0.4);">
        <div class="metric-label" style="color: #F59E0B;">REGULATION</div>
        <div class="metric-value" style="color: #F59E0B;">{sum(a["category"] == "Regulation" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card" style="border-color: rgba(244, 63, 94, 0.4);">
        <div class="metric-label" style="color: #F43F5E;">CYBER & TECH</div>
        <div class="metric-value" style="color: #F43F5E;">{sum(a["category"] == "Cyber and Tech" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card" style="border-color: rgba(16, 185, 129, 0.4);">
        <div class="metric-label" style="color: #10B981;">GLOBAL BANKS</div>
        <div class="metric-value" style="color: #10B981;">{sum(a["category"] == "Global Banks" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

if errors:
    with st.expander("⚠️ SOURCE / API WARNINGS", expanded=False):
        for err in errors:
            st.markdown(f"<div style='font-family: monospace; font-size: 11px; color: #F59E0B;'>• {err}</div>", unsafe_allow_html=True)

# Search Bar
search_query = st.text_input(
    "SEARCH",
    placeholder="QUERY // Filter by institution, regulator (RBI, Basel), keyword (sanctions, model risk)...",
    label_visibility="collapsed"
)

if search_query:
    sq = search_query.lower()
    filtered = [
        a for a in filtered
        if sq in a["title"].lower() or sq in a["description"].lower() or sq in a["source"].lower()
    ]


# ---------------------------------------------------------
# 7. TABBED INTELLIGENCE FEED
# ---------------------------------------------------------

if not filtered:
    st.markdown("""
    <div style="text-align: center; padding: 40px; background: #0D1424; border-radius: 8px; border: 1px dashed rgba(56, 189, 248, 0.3);">
        <div style="font-family: 'JetBrains Mono'; font-size: 13px; color: #94A3B8;">NO AUDIT SIGNALS MATCHING CURRENT CRITERIA</div>
        <div style="font-size: 11px; color: #64748B; margin-top: 5px;">Adjust search query, increase lookback days, or lower the relevance threshold in the sidebar.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    tabs = st.tabs(["// ALL"] + [f"// {c.upper()}" for c in selected_categories])

    def render_articles(rows):
        for art in rows:
            cat = art["category"]
            cat_color = CATEGORY_COLORS.get(cat, "#38BDF8")
            score = art["audit_relevance"]

            if score >= 75:
                score_class = "score-critical"
                score_label = "CRITICAL"
            elif score >= 50:
                score_class = "score-elevated"
                score_label = "ELEVATED"
            else:
                score_class = "score-monitor"
                score_label = "MONITOR"

            formatted_date = art["publishedAt"].replace("T", " ").replace("Z", "")[:16] if art["publishedAt"] else "RECENT"

            st.markdown(f"""
            <div class="article-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <span class="cat-chip" style="background: {cat_color}22; border: 1px solid {cat_color}66; color: {cat_color};">
                            // {cat.upper()}
                        </span>
                        <span class="score-chip {score_class}">
                            {score_label} {score}/100
                        </span>
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 10px; color: #64748B;">
                        {art['source'].upper()} &nbsp;//&nbsp; {formatted_date}
                    </div>
                </div>
                <div style="font-size: 16px; font-weight: 700; color: #FFFFFF; line-height: 1.4; margin-bottom: 8px;">
                    {art['title']}
                </div>
                <div style="font-size: 13px; color: #94A3B8; line-height: 1.5; margin-bottom: 12px;">
                    {art['description']}
                </div>
                <div style="display: flex; justify-content: flex-end; align-items: center;">
                    <a href="{art['url']}" target="_blank" style="text-decoration: none;">
                        <span style="font-family: 'JetBrains Mono'; font-size: 11px; background: #00E5FF; color: #06090F; padding: 4px 12px; border-radius: 4px; font-weight: 700;">
                            READ ORIGINAL ARTICLE ↗
                        </span>
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
                <div style="text-align: center; padding: 30px; background: #0D1424; border-radius: 8px; border: 1px dashed rgba(56, 189, 248, 0.2);">
                    <div style="font-family: 'JetBrains Mono'; font-size: 12px; color: #94A3B8;">NO STORIES IN THIS CATEGORY</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                render_articles(cat_rows)

# ---------------------------------------------------------
# 8. EXPORT DATA SECTION
# ---------------------------------------------------------
st.markdown("<hr style='margin-top: 40px; border-color: rgba(56, 189, 248, 0.2);' />", unsafe_allow_html=True)
col_down1, col_down2 = st.columns([8, 2])
with col_down1:
    st.markdown("""
    <div style="font-family: 'JetBrains Mono'; font-size: 11px; color: #64748B;">
        AEGIS BANKING AUDIT INTELLIGENCE PLATFORM • EXPORT TELEMETRY FOR AUDIT COMMITTEES
    </div>
    """, unsafe_allow_html=True)
with col_down2:
    if filtered:
        df_export = pd.DataFrame(filtered)
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="EXPORT AUDIT CSV",
            data=csv,
            file_name=f"banking_audit_intel_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
