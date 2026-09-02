# Institutional Banking Audit Intelligence Terminal

Real-time surveillance dashboard designed for Bank Internal Audit, Risk Committees, Control Officers, and Supervisory Compliance departments.

## Features
- **0–100 Audit Relevance Engine**: Weighted domain vocabulary covering Basel III/IV, RBI, ECB, AML/KYC, SOX, Model Risk, and Cyber Controls.
- **Parallel Intelligence Fetching**: Multi-threaded category scanning across Transformation, Regulation, People, Cyber & Tech, and Global Banks.
- **Curated Fallback Stream**: Runs out-of-the-box even without an external API key.
- **Audit Committee CSV Export**: Export active findings with risk classifications.

---

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/banking-audit-intelligence.git
   cd banking-audit-intelligence
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Secrets:**
   Open `.streamlit/secrets.toml` and add your NewsAPI key:
   ```toml
   NEWSAPI_KEY = "your_actual_api_key_here"
   ```

4. **Launch Application:**
   ```bash
   streamlit run app.py
   ```

---

## Deploy to Streamlit Community Cloud (Free)

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and click **New App**.
3. Select your repository and specify `app.py` as the main file path.
4. Click **Advanced settings -> Secrets** and paste:
   ```toml
   NEWSAPI_KEY = "your_actual_api_key_here"
   ```
5. Click **Deploy!**
