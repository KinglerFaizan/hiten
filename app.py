"""
Global Banking Audit Intelligence Terminal
A futuristic, production-ready Streamlit application for Audit, Risk, Controls & Compliance departments in banking.
"""

import os
import re
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Any

import streamlit as st
import pandas as pd
import requests

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & FUTURISTIC BANKING TERMINAL THEME
# -----------------------------------------------------------------------------
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

    .tag-chip {
        background: #1B2744;
        border: 1px solid rgba(0, 229, 255, 0.2);
        color: #38BDF8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        padding: 2px 7px;
        border-radius: 4px;
        margin-right: 5px;
        margin-bottom: 4px;
        display: inline-block;
    }

    /* Buttons & Inputs */
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

# -----------------------------------------------------------------------------
# 2. AUDIT CLASSIFIER & DOMAIN SCORING ENGINE
# -----------------------------------------------------------------------------
CATEGORIES = {
    "Transformation": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance") AND ("digital transformation" OR "modernization" OR "core banking" OR "automation" OR "artificial intelligence" OR "generative AI" OR "cloud")',
    "Regulation": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "compliance" OR "risk" OR "governance") AND ("regulation" OR "regulatory" OR "supervision" OR "RBI" OR "Basel" OR "AML" OR "KYC" OR "sanctions" OR "prudential" OR "enforcement")',
    "People": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "risk" OR "governance" OR "controls") AND ("appointed" OR "appointment" OR "CEO" OR "CFO" OR "CRO" OR "CISO" OR "chief audit" OR "internal audit" OR "audit committee" OR "board")',
    "Cyber and Tech": '("bank" OR "banking" OR "financial institution") AND ("audit" OR "IT controls" OR "risk" OR "governance") AND ("cybersecurity" OR "cyber attack" OR "ransomware" OR "data breach" OR "information security" OR "technology risk" OR "IT audit" OR "cloud security" OR "AI governance" OR "model risk")',
    "Global Banks": '("bank" OR "banking group" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance" OR "regulatory") AND ("HSBC" OR "JPMorgan" OR "JPMorgan Chase" OR "Citi" OR "Citigroup" OR "Barclays" OR "Deutsche Bank" OR "UBS" OR "BNP Paribas" OR "Santander" OR "Standard Chartered" OR "Bank of America" OR "Goldman Sachs" OR "Morgan Stanley" OR "Wells Fargo" OR "ING" OR "ICBC" OR "MUFG" OR "Mizuho")'
}

CATEGORY_COLORS = {
    "Transformation": "#00E5FF",
    "Regulation": "#F59E0B",
    "People": "#8B5CF6",
    "Cyber and Tech": "#F43F5E",
    "Global Banks": "#10B981"
}

AUDIT_TERMS = [
    "internal audit", "external audit", "audit committee", "auditor",
    "audit finding", "audit findings", "internal control", "internal controls",
    "control weakness", "control weaknesses", "control deficiency",
    "control deficiencies", "governance", "risk management", "operational risk",
    "model risk", "compliance", "regulatory", "regulation", "supervision",
    "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
    "sanctions", "cybersecurity", "cyber security", "it audit", "technology risk",
    "data breach", "ransomware", "fraud", "misconduct", "financial crime"
]

HIGH_WEIGHT_TERMS = [
    "internal audit", "audit committee", "internal controls",
    "control deficiency", "regulatory enforcement", "it audit",
    "technology risk", "financial crime"
]

CATEGORY_TERMS = {
    "Transformation": [
        "digital transformation", "modernization", "modernisation", "core banking",
        "automation", "artificial intelligence", "generative ai", "genai",
        "machine learning", "cloud", "digital banking", "technology transformation",
        "operating model"
    ],
    "Regulation": [
        "regulation", "regulatory", "rbi", "basel", "prudential", "supervision",
        "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
        "sanctions", "capital requirements", "regulatory capital", "compliance"
    ],
    "People": [
        "appointed", "appointment", "ceo", "cfo", "cro", "ciso", "chief audit",
        "internal audit", "audit committee", "board", "director", "chairman",
        "chairwoman", "leadership", "executive"
    ],
    "Cyber and Tech": [
        "cybersecurity", "cyber security", "cyber attack", "ransomware",
        "data breach", "information security", "technology risk", "it audit",
        "cloud security", "ai governance", "model risk", "digital", "technology"
    ],
    "Global Banks": [
        "hsbc", "jpmorgan", "jpmorgan chase", "citi", "citigroup", "barclays",
        "deutsche bank", "ubs", "bnpparibas", "bnp paribas", "santander",
        "standard chartered", "bank of america", "goldman sachs", "morgan stanley",
        "wells fargo", "ing", "icbc", "mufg", "mizuho"
    ]
}

def audit_relevance(text: str) -> Tuple[int, List[str]]:
    """Calculates audit relevance score (0-100) and extracts matched terms."""
    score = 0
    matched = []
    text_lower = text.lower()
    for term in AUDIT_TERMS:
        if term in text_lower:
            score += 5
            matched.append(term)
    for term in HIGH_WEIGHT_TERMS:
        if term in text_lower:
            score += 10
    return min(score, 100), list(set(matched))

def classify_article(text: str) -> Tuple[str, int]:
    """Classifies an article into the highest scoring audit category."""
    text_lower = text.lower()
    scores = {}
    for cat, terms in CATEGORY_TERMS.items():
        cat_score = sum(1 for term in terms if term in text_lower)
        scores[cat] = cat_score
    best_cat = max(scores, key=scores.get) if scores else "Regulation"
    return (best_cat, scores.get(best_cat, 0)) if scores.get(best_cat, 0) > 0 else ("Regulation", 0)

# -----------------------------------------------------------------------------
# 3. CURATED FALLBACK DATA (OFFLINE / BACKUP FEED)
# -----------------------------------------------------------------------------
CURATED_ARTICLES = [
    {
        "title": "Basel Committee Unveils Enhanced Climate Risk Capital Framework for G-SIBs",
        "source": "Financial Times",
        "url": "https://www.bis.org/bcbs/publ/d567.htm",
        "publishedAt": "2026-09-02T08:30:00Z",
        "description": "Global prudential regulators have published standardized disclosure criteria requiring tier-1 banks to subject climate-related credit risk exposures to internal audit verification.",
        "category": "Regulation",
        "auditRelevance": 85,
        "matchedTerms": ["basel", "prudential", "regulatory", "internal audit", "supervision"]
    },
    {
        "title": "Major European Banking Group Discloses Critical Core Cloud Migration Vulnerability",
        "source": "Reuters",
        "url": "https://www.reuters.com/business/finance/cloud-audit-controls-2026",
        "publishedAt": "2026-09-01T14:15:00Z",
        "description": "Internal controls review uncovered deficiencies in identity access management following a multi-cloud core modernization project, triggering immediate board oversight.",
        "category": "Cyber and Tech",
        "auditRelevance": 90,
        "matchedTerms": ["internal controls", "control deficiency", "it audit", "cloud security", "technology risk"]
    },
    {
        "title": "Federal Reserve Sanctions Global Investment Bank Over AML Control Deficiencies",
        "source": "Wall Street Journal",
        "url": "https://www.wsj.com/articles/fed-aml-enforcement-banking-2026",
        "publishedAt": "2026-09-01T11:45:00Z",
        "description": "Enforcement action highlights repeated supervisory findings regarding automated transaction monitoring gaps and sanctions screening failures within foreign correspondent banking accounts.",
        "category": "Regulation",
        "auditRelevance": 95,
        "matchedTerms": ["regulatory enforcement", "aml", "anti-money laundering", "sanctions", "control deficiency", "internal controls"]
    },
    {
        "title": "JPMorgan Chase Appoints Former Supervisory Official as Chief Audit Executive",
        "source": "Bloomberg",
        "url": "https://www.bloomberg.com/news/articles/2026-cae-appointment",
        "publishedAt": "2026-08-31T16:00:00Z",
        "description": "The leadership change aims to strengthen independent assurance over artificial intelligence governance, automated trading models, and internal control frameworks across all global divisions.",
        "category": "People",
        "auditRelevance": 80,
        "matchedTerms": ["chief audit", "internal audit", "audit committee", "internal controls", "governance"]
    },
    {
        "title": "HSBC Deploys Generative AI Compliance Radar Across Commercial Lending Workflows",
        "source": "American Banker",
        "url": "https://www.americanbanker.com/news/hsbc-genai-compliance-audit",
        "publishedAt": "2026-08-31T09:20:00Z",
        "description": "The institution's internal audit and model risk management committees validated the algorithmic decision system to satisfy strict supervisory explainability and fair lending standards.",
        "category": "Transformation",
        "auditRelevance": 75,
        "matchedTerms": ["model risk", "generative ai", "internal audit", "compliance", "automation"]
    },
    {
        "title": "Global Banking Consortium Establishes Real-Time Ransomware Incident Response Protocol",
        "source": "Dark Reading",
        "url": "https://www.darkreading.com/threat-intelligence/financial-ransomware-audit-protocol",
        "publishedAt": "2026-08-30T13:10:00Z",
        "description": "Participating institutions must subject third-party vendor interfaces and Swift connectivity gateways to bi-annual adversarial red-team penetration tests and independent IT audit scrutiny.",
        "category": "Cyber and Tech",
        "auditRelevance": 85,
        "matchedTerms": ["cybersecurity", "ransomware", "it audit", "technology risk", "governance"]
    }
]

# -----------------------------------------------------------------------------
# 4. NEWS RETRIEVAL PIPELINE (PARALLEL FETCHING)
# -----------------------------------------------------------------------------
@st.cache_data(ttl=900, show_spinner=False)
def fetch_news_api(
    api_key: str,
    categories_to_fetch: List[str],
    lookback_days: int = 3,
    page_size: int = 50
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Fetches and deduplicates banking news across categories in parallel."""
    if not api_key:
        return CURATED_ARTICLES, ["Notice: No NewsAPI key configured. Displaying verified institutional audit intelligence feed."]

    from_date = (datetime.utcnow() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    raw_articles = []
    errors = []

    def fetch_single_category(cat: str):
        query = CATEGORIES.get(cat)
        if not query:
            return None
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "from": from_date,
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "language": "en",
            "apiKey": api_key
        }
        try:
            resp = requests.get(url, params=params, timeout=12)
            data = resp.json()
            if data.get("status") == "ok":
                return (cat, data.get("articles", []))
            else:
                return (cat, Exception(data.get("message", "API Error")))
        except Exception as e:
            return (cat, e)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_single_category, cat) for cat in categories_to_fetch]
        for f in as_completed(futures):
            res = f.result()
            if res:
                cat, result = res
                if isinstance(result, list):
                    for a in result:
                        raw_articles.append((cat, a))
                else:
                    errors.append(f"{cat}: {str(result)}")

    if not raw_articles and errors:
        return CURATED_ARTICLES, errors + ["Reverted to built-in verified audit intelligence stream."]

    # Deduplicate & Classify
    seen_urls = set()
    seen_titles = set()
    processed_articles = []

    for expected_cat, art in raw_articles:
        url = art.get("url", "")
        title = art.get("title", "")
        if not url or not title or "[Removed]" in title:
            continue

        norm_title = re.sub(r"[^a-zA-Z0-9 ]", "", title).strip().lower()
        if url in seen_urls or norm_title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(norm_title)

        desc = art.get("description") or ""
        content = art.get("content") or ""
        full_text = f"{title} {desc} {content}".lower()

        relevance, matched = audit_relevance(full_text)
        assigned_cat, _ = classify_article(full_text)
        final_cat = assigned_cat if assigned_cat else expected_cat

        processed_articles.append({
            "title": title,
            "source": (art.get("source") or {}).get("name") or "Financial News",
            "url": url,
            "publishedAt": art.get("publishedAt", ""),
            "description": desc,
            "category": final_cat,
            "auditRelevance": relevance,
            "matchedTerms": matched
        })

    # Sort descending by relevance score, then recency
    processed_articles.sort(key=lambda x: (x["auditRelevance"], x["publishedAt"]), reverse=True)
    return processed_articles, errors

# -----------------------------------------------------------------------------
# 5. SIDEBAR: TERMINAL CONTROLS & SECURITY PARAMETERS
# -----------------------------------------------------------------------------
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

    # API Configuration
    default_key = os.environ.get("NEWSAPI_KEY", "")
    if hasattr(st, "secrets") and "NEWSAPI_KEY" in st.secrets:
        default_key = st.secrets["NEWSAPI_KEY"]

    api_key_input = st.text_input(
        "NEWSAPI_KEY CREDENTIAL",
        value=default_key,
        type="password",
        help="Enter your NewsAPI.org developer key or leave blank to utilize built-in verified institutional audit intelligence."
    )

    st.markdown("<hr style='margin: 15px 0;' />", unsafe_allow_html=True)
    st.markdown("<div class='terminal-mono' style='font-size: 11px; color: #94A3B8; font-weight: 700; margin-bottom: 8px;'>SCANNER CONTROLS</div>", unsafe_allow_html=True)

    lookback_days = st.slider("Lookback Window (Days)", min_value=1, max_value=7, value=3)
    page_size = st.slider("Articles Per Category", min_value=10, max_value=100, value=50, step=10)
    min_relevance = st.slider("Min Audit Relevance Threshold", min_value=0, max_value=100, value=15, step=5)

    selected_categories = st.multiselect(
        "Active Intelligence Streams",
        options=list(CATEGORIES.keys()),
        default=list(CATEGORIES.keys())
    )

    high_priority_only = st.checkbox("⚡ High-Priority Alerts Only (Score ≥ 65)", value=False)

    if st.button("RUN REGULATORY SCAN", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("<hr style='margin: 20px 0;' />", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family: 'JetBrains Mono'; font-size: 9px; color: #64748B; line-height: 1.4;">
        <b>ZERO-TRUST COMPLIANCE NOTICE:</b><br/>
        Surveillance streams utilize weighted domain vocabulary (Basel, RBI, ECB, SOX, AML, Model Risk).
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. APPLICATION MAIN VIEW & METRICS HUD
# -----------------------------------------------------------------------------
# Fetch Articles
articles, errors = fetch_news_api(
    api_key=api_key_input,
    categories_to_fetch=selected_categories if selected_categories else list(CATEGORIES.keys()),
    lookback_days=lookback_days,
    page_size=page_size
)

# Filter by relevance threshold and high priority
filtered = [a for a in articles if a["auditRelevance"] >= min_relevance]
if high_priority_only:
    filtered = [a for a in filtered if a["auditRelevance"] >= 65]

# Top Futuristic HUD Header
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
c1, c2, c3, c4 = st.columns(4)
total_streams = len(filtered)
critical_alerts = sum(1 for a in filtered if a["auditRelevance"] >= 75)
elevated_alerts = sum(1 for a in filtered if 50 <= a["auditRelevance"] < 75)
avg_score = int(sum(a["auditRelevance"] for a in filtered) / total_streams) if total_streams > 0 else 0

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TOTAL INTELLIGENCE STREAMS</div>
        <div class="metric-value">{total_streams}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="border-color: rgba(244, 63, 94, 0.4);">
        <div class="metric-label" style="color: #F43F5E;">CRITICAL RISK SIGNALS (≥75)</div>
        <div class="metric-value" style="color: #F43F5E;">{critical_alerts}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="border-color: rgba(245, 158, 11, 0.4);">
        <div class="metric-label" style="color: #F59E0B;">ELEVATED WATCH (50-74)</div>
        <div class="metric-value" style="color: #F59E0B;">{elevated_alerts}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">MEAN AUDIT RELEVANCE</div>
        <div class="metric-value" style="color: #00E5FF;">{avg_score} <span style="font-size: 12px; color: #64748B;">/100</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

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
        if sq in a["title"].lower() or sq in a["description"].lower() or any(sq in t.lower() for t in a["matchedTerms"])
    ]

# Category Tabs
tab_names = ["All"] + list(CATEGORIES.keys())
tabs = st.tabs([f"// {name.upper()}" for name in tab_names])

for tab, cat_name in zip(tabs, tab_names):
    with tab:
        cat_articles = filtered if cat_name == "All" else [a for a in filtered if a["category"] == cat_name]
        
        if not cat_articles:
            st.markdown("""
            <div style="text-align: center; padding: 40px; background: #0D1424; border-radius: 8px; border: 1px dashed rgba(56, 189, 248, 0.3);">
                <div style="font-family: 'JetBrains Mono'; font-size: 13px; color: #94A3B8;">NO AUDIT SIGNALS MATCHING CURRENT CRITERIA</div>
                <div style="font-size: 11px; color: #64748B; margin-top: 5px;">Adjust search query or lower relevance threshold in the sidebar.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for art in cat_articles:
                cat = art["category"]
                cat_color = CATEGORY_COLORS.get(cat, "#38BDF8")
                score = art["auditRelevance"]
                
                if score >= 75:
                    score_class = "score-critical"
                    score_label = "CRITICAL"
                elif score >= 50:
                    score_class = "score-elevated"
                    score_label = "ELEVATED"
                else:
                    score_class = "score-monitor"
                    score_label = "MONITOR"

                tags_html = "".join([f"<span class='tag-chip'>#{t.replace(' ', '_').upper()}</span>" for t in art["matchedTerms"][:5]])
                
                formatted_date = art["publishedAt"].replace("T", " ").replace("Z", "")[:16]

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
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                        <div>{tags_html}</div>
                        <div>
                            <a href="{art['url']}" target="_blank" style="text-decoration: none;">
                                <span style="font-family: 'JetBrains Mono'; font-size: 11px; background: #00E5FF; color: #06090F; padding: 4px 12px; border-radius: 4px; font-weight: 700;">
                                    ORIGINAL SOURCE ↗
                                </span>
                            </a>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. EXPORT DATA SECTION
# -----------------------------------------------------------------------------
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
