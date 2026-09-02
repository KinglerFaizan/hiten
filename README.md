# 🏦 Global Banking Audit Intelligence (Android)

A modern Android application built with **Kotlin** and **Jetpack Compose** that finds, scores, and classifies **global banking news relevant to Audit, Risk, Controls, and Compliance departments**.

Rewritten from the original Python/Streamlit prototype into a production-ready, reactive Android application.

## Core Features

- **5 Targeted Audit Categories**:
  1. **Transformation**: Digital transformation, core banking modernization, AI/GenAI, automation, cloud infrastructure.
  2. **Regulation**: RBI, Basel Committee, banking prudential regulation, AML/KYC, international sanctions, enforcement.
  3. **People**: C-suite appointments (CEO, CFO, CRO, CISO), Chief Audit Executive leadership, Audit Committees, and Board governance.
  4. **Cyber and Tech**: Cybersecurity, ransomware, IT audit, technology risk, cloud security, AI governance, and algorithmic model risk.
  5. **Global Banks**: Tier-1 international institutions (HSBC, JPMorgan Chase, Citi, Barclays, Deutsche Bank, UBS, BNP Paribas, Santander, Standard Chartered, Bank of America, Goldman Sachs, Morgan Stanley, Wells Fargo, etc.).
- **Transparent Audit Relevance Scoring (0–100)**:
  - Uses weighted domain vocabulary (`internal controls`, `control deficiency`, `audit committee`, `regulatory enforcement`, `model risk`, etc.) to score stories.
  - Automatically filters out general/retail banking noise.
- **Rule-Based Classification Engine**:
  - Scores category terms across article titles, descriptions, and content.
- **Concurrent Coroutine Architecture**:
  - Parallel queries executed concurrently via Kotlin Coroutines (`async`/`awaitAll`), preserving the original `ThreadPoolExecutor` design.
- **Deduplication & Sorting**:
  - Intelligent deduplication by URL and normalized title.
  - Sorted descending by audit relevance score and publication recency.
- **Search & Settings Customization**:
  - Configurable NewsAPI key with fallback to built-in curated banking audit intelligence.
  - Interactive sliders for lookback window (1–7 days), articles per category (10–100), and minimum relevance threshold.
  - Category multi-selection toggle.
- **Interactive UI & Bookmarking**:
  - Tab navigation ("All", individual categories, and "Bookmarks").
  - Instant full-text search across titles, descriptions, and matched keywords.
  - Article detail inspection showing triggered vocabulary terms and score analysis.
  - Direct external article launching and native Android sharing.

## Architecture & Technology Stack

- **Platform**: Android (SDK 36, Min SDK 26)
- **Language**: Kotlin 2.2
- **UI Framework**: Jetpack Compose (Material Design 3)
- **Asynchronous Execution**: Kotlin Coroutines & StateFlow
- **Networking**: Retrofit 2 + OkHttp 4 + Gson Converter
- **Build System**: Gradle 9.3.1 with Kotlin DSL

## Project Structure

```text
├── app/
│   ├── src/main/
│   │   ├── java/com/example/audit/
│   │   │   ├── data/
│   │   │   │   ├── AuditRepository.kt
│   │   │   │   └── CuratedAuditData.kt
│   │   │   ├── model/
│   │   │   │   ├── AuditClassifier.kt
│   │   │   │   └── AuditModels.kt
│   │   │   ├── network/
│   │   │   │   └── NewsApiService.kt
│   │   │   ├── ui/
│   │   │   │   ├── theme/
│   │   │   │   │   ├── Color.kt
│   │   │   │   │   └── Theme.kt
│   │   │   │   ├── AuditScreen.kt
│   │   │   │   └── AuditViewModel.kt
│   │   │   └── MainActivity.kt
│   │   └── res/
│   │       ├── drawable/
│   │       ├── mipmap-anydpi-v26/
│   │       └── values/
│   └── build.gradle.kts
├── gradle/
│   └── libs.versions.toml
├── build.gradle.kts
├── settings.gradle.kts
└── metadata.json
```
