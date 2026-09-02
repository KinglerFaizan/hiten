package com.example.audit.model

object AuditClassifier {

    val CATEGORIES = mapOf(
        "Transformation" to """("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance") AND ("digital transformation" OR "modernization" OR "core banking" OR "automation" OR "artificial intelligence" OR "generative AI" OR "cloud")""",
        "Regulation" to """("bank" OR "banking" OR "financial institution") AND ("audit" OR "internal controls" OR "compliance" OR "risk" OR "governance") AND ("regulation" OR "regulatory" OR "supervision" OR "RBI" OR "Basel" OR "AML" OR "KYC" OR "sanctions" OR "prudential" OR "enforcement")""",
        "People" to """("bank" OR "banking" OR "financial institution") AND ("audit" OR "risk" OR "governance" OR "controls") AND ("appointed" OR "appointment" OR "CEO" OR "CFO" OR "CRO" OR "CISO" OR "chief audit" OR "internal audit" OR "audit committee" OR "board")""",
        "Cyber and Tech" to """("bank" OR "banking" OR "financial institution") AND ("audit" OR "IT controls" OR "risk" OR "governance") AND ("cybersecurity" OR "cyber attack" OR "ransomware" OR "data breach" OR "information security" OR "technology risk" OR "IT audit" OR "cloud security" OR "AI governance" OR "model risk")""",
        "Global Banks" to """("bank" OR "banking group" OR "financial institution") AND ("audit" OR "internal controls" OR "risk" OR "governance" OR "regulatory") AND ("HSBC" OR "JPMorgan" OR "JPMorgan Chase" OR "Citi" OR "Citigroup" OR "Barclays" OR "Deutsche Bank" OR "UBS" OR "BNP Paribas" OR "Santander" OR "Standard Chartered" OR "Bank of America" OR "Goldman Sachs" OR "Morgan Stanley" OR "Wells Fargo" OR "ING" OR "ICBC" OR "MUFG" OR "Mizuho")"""
    )

    val CATEGORY_ORDER = listOf(
        "Transformation",
        "Regulation",
        "People",
        "Cyber and Tech",
        "Global Banks"
    )

    // Extra audit vocabulary is used to remove ordinary banking stories.
    val AUDIT_TERMS = listOf(
        "internal audit", "external audit", "audit committee", "auditor",
        "audit finding", "audit findings", "internal control", "internal controls",
        "control weakness", "control weaknesses", "control deficiency",
        "control deficiencies", "governance", "risk management", "operational risk",
        "model risk", "compliance", "regulatory", "regulation", "supervision",
        "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
        "sanctions", "cybersecurity", "cyber security", "it audit", "technology risk",
        "data breach", "ransomware", "fraud", "misconduct", "financial crime"
    )

    val HIGH_WEIGHT_TERMS = listOf(
        "internal audit", "audit committee", "internal controls",
        "control deficiency", "regulatory enforcement", "it audit",
        "technology risk", "financial crime"
    )

    val CATEGORY_TERMS = mapOf(
        "Transformation" to listOf(
            "digital transformation", "modernization", "modernisation", "core banking",
            "automation", "artificial intelligence", "generative ai", "genai",
            "machine learning", "cloud", "digital banking", "technology transformation",
            "operating model"
        ),
        "Regulation" to listOf(
            "regulation", "regulatory", "rbi", "basel", "prudential", "supervision",
            "supervisory", "enforcement", "aml", "anti-money laundering", "kyc",
            "sanctions", "capital requirements", "regulatory capital", "compliance"
        ),
        "People" to listOf(
            "appointed", "appointment", "ceo", "cfo", "cro", "ciso", "chief audit",
            "internal audit", "audit committee", "board", "director", "chairman",
            "chairwoman", "leadership", "executive"
        ),
        "Cyber and Tech" to listOf(
            "cybersecurity", "cyber security", "cyber attack", "ransomware",
            "data breach", "information security", "technology risk", "it audit",
            "cloud security", "ai governance", "model risk", "digital", "technology"
        ),
        "Global Banks" to listOf(
            "hsbc", "jpmorgan", "jpmorgan chase", "citi", "citigroup", "barclays",
            "deutsche bank", "ubs", "bnpparibas", "bnp paribas", "santander",
            "standard chartered", "bank of america", "goldman sachs", "morgan stanley",
            "wells fargo", "ing", "icbc", "mufg", "mizuho"
        )
    )

    fun normalizeText(title: String?, description: String?, content: String?): String {
        return listOfNotNull(title, description, content).joinToString(" ").lowercase()
    }

    fun auditRelevance(text: String): Pair<Int, List<String>> {
        var score = 0
        val matched = mutableListOf<String>()

        for (term in AUDIT_TERMS) {
            if (text.contains(term)) {
                score += 5
                matched.add(term)
            }
        }

        for (term in HIGH_WEIGHT_TERMS) {
            if (text.contains(term)) {
                score += 10
            }
        }

        return Pair(score.coerceAtMost(100), matched.distinct())
    }

    fun classifyArticle(text: String): Pair<String, Int> {
        val scores = mutableMapOf<String, Int>()

        for ((category, terms) in CATEGORY_TERMS) {
            var catScore = 0
            for (term in terms) {
                if (text.contains(term)) {
                    catScore += 1
                }
            }
            scores[category] = catScore
        }

        var bestCategory = "Regulation"
        var maxScore = -1

        for ((cat, score) in scores) {
            if (score > maxScore) {
                maxScore = score
                bestCategory = cat
            }
        }

        if (maxScore <= 0) {
            bestCategory = "Regulation"
            maxScore = 0
        }

        return Pair(bestCategory, maxScore)
    }
}
