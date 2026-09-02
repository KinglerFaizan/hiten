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
# 1. APP CONFIGURATION & EDITORIAL FUTURISTIC PALETTE
# ---------------------------------------------------------

st.set_page_config(
    page_title="Audit Intel | Global Banking Briefing",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# High-End Modern Editorial Theme: Warm ivory canvas, rich obsidian ink, warm amber accent, rounded cards
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Canvas */
    .stApp {
        background-color: #F7F5F0;
        color: #1C1917;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #EFECE5;
        border-right: 1px solid #E4DFD5;
    }
    [data-testid="stSidebar"] hr {
        border-color: #E0DBD0;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #1C1917 !important;
    }

    /* Editorial Briefing Header */
    .briefing-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: #B45309;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .briefing-headline {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 38px;
        font-weight: 600;
        color: #18181B;
        letter-spacing: -0.8px;
        line-height: 1.15;
        margin-bottom: 6px;
    }
    .briefing-subhead {
        font-size: 14.5px;
        color: #78716C;
        margin-bottom: 24px;
        font-weight: 400;
    }

    /* Metric Stat Cards */
    .editorial-metric {
        background: #FFFFFF;
        border: 1px solid #E6E1D7;
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .editorial-metric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.04);
    }
    .metric-label {
        font-size: 11.5px;
        font-weight: 600;
        color: #78716C;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .metric-count {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 28px;
        font-weight: 600;
        color: #18181B;
    }

    /* Pill-style Tabs matching Image */
    div[data-testid="stTabs"] {
        margin-top: 10px;
        margin-bottom: 24px;
    }
    div[data-testid="stTabs"] [role="tablist"] {
        gap: 10px;
        border-bottom: none;
    }
    div[data-testid="stTabs"] button[role="tab"] {
        border-radius: 30px !important;
        padding: 7px 20px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E6E1D7 !important;
        color: #57534E !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stTabs"] button[role="tab"]:hover {
        border-color: #B45309 !important;
        color: #1C1917 !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background-color: #18181B !important;
        border-color: #18181B !important;
        color: #FFFFFF !important;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.12) !important;
    }

    /* Article Card - Exactly matching the uploaded style */
    .article-briefing-card {
        background: #FFFFFF;
        border: 1px solid #E6E1D7;
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        transition: box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .article-briefing-card:hover {
        border-color: #D6D0C4;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
    }
    .card-top-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 14px;
    }
    .icon-badge {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background-color: #F0FDF4;
        border: 1.5px solid #BBF7D0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #15803D;
        font-size: 16px;
        flex-shrink: 0;
    }
    .meta-text-top {
        display: flex;
        flex-direction: column;
        line-height: 1.35;
    }
    .category-time {
        font-size: 11px;
        font-weight: 700;
        color: #0F766E;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .source-name {
        font-size: 13.5px;
        font-weight: 600;
        color: #78716C;
    }

    /* Increased, Natural Font Sizes */
    .card-title-text {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 22px;
        font-weight: 600;
        color: #18181B;
        line-height: 1.35;
        letter-spacing: -0.2px;
        margin-bottom: 12px;
    }
    .card-summary-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 16.5px;
        font-weight: 400;
        color: #44403C;
        line-height: 1.65;
        margin-bottom: 18px;
    }

    /* Card Footer Actions */
    .card-footer-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 14px;
        border-top: 1px solid #F3EFE8;
        font-size: 13px;
    }
    .tag-badge {
        font-size: 11.5px;
        font-weight: 600;
        color: #B45309;
        background: #FEF3C7;
        padding: 3px 10px;
        border-radius: 20px;
    }
    .read-source-link {
        font-size: 13px;
        font-weight: 600;
        color: #18181B;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: color 0.15s ease;
    }
    .read-source-link:hover {
        color: #B45309;
        text-decoration: underline;
    }

    /* Streamlit Input Overrides */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        border: 1px solid #E6E1D7 !important;
        color: #18181B !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14.5px !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #B45309 !important;
        box-shadow: 0 0 0 1px #B45309 !important;
    }
    .stButton>button {
        background-color: #18181B;
        color: #FFFFFF;
        border: 1px solid #18181B;
        border-radius: 24px;
        font-weight: 600;
        font-size: 13.5px;
        padding: 8px 20px;
        transition: all 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #27272A;
        border-color: #27272A;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 2. BANKING AUDIT CATEGORIES & QUERIES (NO CYBER & TECH)
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
    "Global Banks": {
        "query": '("bank" OR "banking group" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance" OR "regulatory") AND ("HSBC" OR "JPMorgan" OR "JPMorgan Chase" OR "Citi" OR "Citigroup" OR "Barclays" OR "Deutsche Bank" OR "UBS" OR "BNP Paribas" OR "Santander" OR "Standard Chartered" OR "Bank of America" OR "Goldman Sachs" OR "Morgan Stanley" OR "Wells Fargo" OR "ING" OR "ICBC" OR "MUFG" OR "Mizuho")'
    },
}

# Audit vocabulary for relevance scoring
AUDIT_TERMS = [
    "internal audit", "external audit", "audit committee", "auditor",
    "audit finding", "audit findings", "internal control", "internal controls",
    "control weakness", "control weaknesses", "control deficiency",
    "control deficiencies", "governance", "risk management", "operational risk",
    "model risk", "compliance", "regulatory", "regulation", "supervision",
    "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
    "sanctions", "fraud", "misconduct", "financial crime",
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
    """Use Streamlit secrets/env first; sidebar entry is the fallback."""
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
    """Simple, transparent audit relevance score."""
    score = 0
    for term in AUDIT_TERMS:
        if term in text:
            score += 5

    # Stronger signals get additional weight
    for term in [
        "internal audit", "audit committee", "internal controls",
        "control deficiency", "regulatory enforcement",
        "model risk", "financial crime",
    ]:
        if term in text:
            score += 10

    return min(score, 100)


def classify_article(article):
    """Classify using transparent keyword scoring."""
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
    Fetch all targeted banking searches in parallel.
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

    # Deduplicate by URL first, then by normalized title
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

        # Only retain stories with a meaningful audit/risk/control signal
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
            "source": source.get("name") or "Institutional Source",
            "publishedAt": published,
            "url": article.get("url") or "",
            "author": article.get("author") or "",
        })

    cleaned.sort(key=lambda x: (x["audit_relevance"], x["publishedAt"]), reverse=True)
    return cleaned, errors


def format_relative_time(pub_date_str):
    """Formats relative date nicely (e.g. '3 days ago', '1 week ago')."""
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
            return "1 day ago"
        elif days < 7:
            return f"{days} days ago"
        elif days < 14:
            return "1 week ago"
        else:
            return f"{days // 7} weeks ago"
    except Exception:
        return pub_date_str[:10] if len(pub_date_str) >= 10 else "Recent"


# ---------------------------------------------------------
# 4. SIDEBAR: CLEAN MINIMAL CONTROLS (NO THRESHOLD SCROLLBAR)
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div style="padding-top: 4px; margin-bottom: 16px;">
        <div style="font-family: 'Newsreader', Georgia, serif; font-size: 22px; font-weight: 600; color: #18181B;">Audit Intel</div>
        <div style="font-size: 11.5px; color: #B45309; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase;">Banking Surveillance Briefing</div>
    </div>
    """, unsafe_allow_html=True)

    api_key = get_api_key()

    if not api_key:
        api_key = st.text_input(
            "NewsAPI Key",
            type="password",
            placeholder="Enter API key...",
            help="Configurable via secrets.toml or enter here for the session.",
        )

    st.markdown("<hr style='margin: 12px 0;' />", unsafe_allow_html=True)

    lookback_days = st.slider(
        "Lookback Window (Days)",
        min_value=1,
        max_value=7,
        value=3,
    )

    page_size = st.slider(
        "Stories Per Category",
        min_value=10,
        max_value=100,
        value=50,
        step=10,
    )

    selected_categories = st.multiselect(
        "Active Categories",
        options=list(CATEGORIES.keys()),
        default=list(CATEGORIES.keys()),
    )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    refresh = st.button("Update Briefing", use_container_width=True)

    st.markdown("<hr style='margin: 20px 0;' />", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 12px; color: #78716C; line-height: 1.55;">
        <b>Scope of Surveillance:</b><br/>
        Internal Audit, Board Governance, Basel Prudential Supervision, RBI Directions, Executive Appointments, and Large Bank Controls.
    </div>
    """, unsafe_allow_html=True)

if not api_key:
    st.info("💡 Please enter your NewsAPI key in the sidebar or configure API_KEY in Streamlit secrets.")
    st.stop()


# ---------------------------------------------------------
# 5. DATA INGESTION & FILTERING
# ---------------------------------------------------------

if refresh or "news_loaded" not in st.session_state:
    with st.spinner("Compiling this week's audit intelligence briefing..."):
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
# 6. EDITORIAL BRIEFING HEADER & STATS
# ---------------------------------------------------------

st.markdown(f"""
<div style="margin-bottom: 20px;">
    <div class="briefing-tag">AUDIT INTEL</div>
    <div class="briefing-headline">This week's briefing</div>
    <div class="briefing-subhead">{len(filtered)} items &nbsp;·&nbsp; updated daily &nbsp;·&nbsp; verified banking internal controls & regulatory surveillance</div>
</div>
""", unsafe_allow_html=True)

# Clean KPI Stat Strip (4 banking categories + Total)
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f"""
    <div class="editorial-metric">
        <div class="metric-label">Total Briefing</div>
        <div class="metric-count">{len(filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="editorial-metric">
        <div class="metric-label">Transformation</div>
        <div class="metric-count">{sum(a["category"] == "Transformation" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="editorial-metric">
        <div class="metric-label">Regulation</div>
        <div class="metric-count">{sum(a["category"] == "Regulation" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="editorial-metric">
        <div class="metric-label">People</div>
        <div class="metric-count">{sum(a["category"] == "People" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class="editorial-metric">
        <div class="metric-label">Global Banks</div>
        <div class="metric-count">{sum(a["category"] == "Global Banks" for a in filtered)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

if errors:
    with st.expander("Feed Diagnostic Notices", expanded=False):
        for err in errors:
            st.markdown(f"<div style='font-size: 12px; color: #B45309;'>• {err}</div>", unsafe_allow_html=True)

# Instant Search Bar
search_query = st.text_input(
    "Filter Briefing",
    placeholder="Search briefing (e.g. HDFC, Basel, RBI, JPMorgan, Internal Audit)...",
    label_visibility="collapsed"
)

if search_query:
    sq = search_query.lower()
    filtered = [
        a for a in filtered
        if sq in a["title"].lower() or sq in a["description"].lower() or sq in a["source"].lower()
    ]


# ---------------------------------------------------------
# 7. EDITORIAL PILL TABS & BRIEFING CARDS
# ---------------------------------------------------------

if not filtered:
    st.markdown("""
    <div style="text-align: center; padding: 48px; background: #FFFFFF; border-radius: 16px; border: 1px dashed #E6E1D7; margin-top: 14px;">
        <div style="font-family: 'Newsreader', Georgia, serif; font-size: 20px; font-weight: 600; color: #18181B;">No briefing stories found</div>
        <div style="font-size: 14px; color: #78716C; margin-top: 6px;">Try expanding the lookback window or broadening search keywords in the sidebar.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    tabs = st.tabs(["All"] + [f"{c}" for c in selected_categories])

    def render_briefing_cards(rows):
        for art in rows:
            cat = art["category"]
            rel_time = format_relative_time(art["publishedAt"])
            source_title = art["source"]
            score = art["audit_relevance"]

            description_text = art["description"] if art["description"] else "Independent institutional briefing coverage. Select below to review the full verified source documentation."

            st.markdown(f"""
            <div class="article-briefing-card">
                <div class="card-top-row">
                    <div class="icon-badge">
                        <span>🛡️</span>
                    </div>
                    <div class="meta-text-top">
                        <span class="category-time">{cat} &nbsp;·&nbsp; {rel_time}</span>
                        <span class="source-name">{source_title}</span>
                    </div>
                </div>
                <div class="card-title-text">
                    {art['title']}
                </div>
                <div class="card-summary-text">
                    {description_text}
                </div>
                <div class="card-footer-row">
                    <div>
                        <span class="tag-badge">Audit Score: {score}/100</span>
                    </div>
                    <div>
                        <a href="{art['url']}" target="_blank" class="read-source-link">
                            <span>Read source</span>
                            <span style="font-size: 14px;">↗</span>
                        </a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[0]:
        render_briefing_cards(filtered)

    for tab, category in zip(tabs[1:], selected_categories):
        with tab:
            cat_rows = [a for a in filtered if a["category"] == category]
            if not cat_rows:
                st.markdown(f"""
                <div style="text-align: center; padding: 36px; background: #FFFFFF; border-radius: 16px; border: 1px dashed #E6E1D7;">
                    <div style="font-family: 'Newsreader', Georgia, serif; font-size: 16px; color: #78716C;">No items currently logged under {category}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                render_briefing_cards(cat_rows)


# ---------------------------------------------------------
# 8. EXPORT SECTION
# ---------------------------------------------------------
st.markdown("<hr style='margin-top: 36px; border-color: #E6E1D7;' />", unsafe_allow_html=True)
col_down1, col_down2 = st.columns([8, 2])
with col_down1:
    st.markdown("""
    <div style="font-size: 12.5px; color: #78716C;">
        Audit Intel Briefing • Curated intelligence feed for Audit Committees and Chief Risk Officers
    </div>
    """, unsafe_allow_html=True)
with col_down2:
    if filtered:
        df_export = pd.DataFrame(filtered)
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"audit_intel_briefing_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
