package com.example.audit.data

import com.example.audit.model.AuditArticle

object CuratedAuditData {

    fun getSampleArticles(): List<AuditArticle> {
        return listOf(
            AuditArticle(
                title = "Basel Committee Flags Cloud Outage Exposure and Technology Risk in Tier-1 Bank Internal Controls",
                description = "Prudential supervisors and the Basel Committee on Banking Supervision issue fresh supervisory guidance mandating stricter operational risk and internal control testing over multi-cloud core banking architectures.",
                content = "Regulators across the G10 expressed growing concern over concentration risk in third-party cloud service providers. The audit committee and internal audit departments are instructed to evaluate disaster recovery failovers, IT audit frameworks, and operational resilience against systemic shocks.",
                url = "https://www.bis.org/press/p240901.htm",
                sourceName = "Bank for International Settlements",
                publishedAt = "2026-09-01T14:30:00Z",
                author = "Regulatory Policy Division",
                category = "Regulation",
                auditRelevance = 85,
                categoryScore = 6,
                matchedTerms = listOf("internal controls", "operational risk", "supervision", "basel", "it audit", "technology risk")
            ),
            AuditArticle(
                title = "JPMorgan Chase Revamps Internal Audit Protocols for Generative AI and Algorithmic Model Risk",
                description = "Wall Street's largest bank deploys continuous automated auditing models to supervise AI governance and prevent control deficiencies in automated credit and fraud surveillance engines.",
                content = "The Global Chief Audit Executive at JPMorgan Chase emphasized the bank's transition toward real-time algorithmic auditing. The new internal controls framework tests generative AI output drift, data lineage, and model risk compliance across consumer and corporate lending portfolios.",
                url = "https://www.jpmorganchase.com/news",
                sourceName = "Financial Times",
                publishedAt = "2026-09-01T11:15:00Z",
                author = "Sarah Jenkins",
                category = "Global Banks",
                auditRelevance = 90,
                categoryScore = 7,
                matchedTerms = listOf("internal audit", "internal controls", "model risk", "control deficiency", "fraud", "governance")
            ),
            AuditArticle(
                title = "RBI Directs Supervised Entities to Rectify IT Audit Control Weaknesses in Core Banking Migration",
                description = "The Reserve Bank of India mandates quarterly board and audit committee attestations for digital transformation roadmaps following supervisory findings on cyber resilience and core ledger integrity.",
                content = "Under updated regulatory enforcement frameworks, banking institutions must furnish independent IT audit reports verifying core banking modernization milestones, AML screening latency, and data protection safeguards prior to regulatory approvals.",
                url = "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx",
                sourceName = "Economic Times",
                publishedAt = "2026-08-31T09:00:00Z",
                author = "Anand Sharma",
                category = "Transformation",
                auditRelevance = 80,
                categoryScore = 5,
                matchedTerms = listOf("audit committee", "it audit", "control weakness", "regulatory enforcement", "rbi", "aml")
            ),
            AuditArticle(
                title = "HSBC Board Appoints New Chief Audit Executive Amid Comprehensive Governance Realignment",
                description = "The Group Audit Committee announces the appointment of a veteran financial crime auditor as Group Head of Internal Audit to strengthen risk management oversight across transatlantic divisions.",
                content = "Reporting directly to the Chair of the Audit Committee and functionally to the Group CEO, the new Chief Audit Executive will lead over 1,200 audit professionals overseeing compliance with global sanctions, AML monitoring, and digital operational resilience.",
                url = "https://www.hsbc.com/news-and-media",
                sourceName = "Bloomberg Law",
                publishedAt = "2026-08-30T16:45:00Z",
                author = "Claire Delacroix",
                category = "People",
                auditRelevance = 75,
                categoryScore = 5,
                matchedTerms = listOf("internal audit", "audit committee", "chief audit", "financial crime", "sanctions", "governance")
            ),
            AuditArticle(
                title = "European Central Bank Penalizes Cross-Border Bank for Critical AML and Sanctions Control Deficiencies",
                description = "ECB Banking Supervision imposes supervisory corrective measures following on-site audit findings identifying systematic gaps in automated sanctions screening and transaction monitoring.",
                content = "The supervisory sanctions notice highlighted multi-year control deficiencies in correspondent banking validation. The institution's internal audit department had flagged control weaknesses that executive leadership failed to remediate within prescribed prudential timelines.",
                url = "https://www.bankingsupervision.europa.eu",
                sourceName = "Reuters Financial",
                publishedAt = "2026-08-29T13:20:00Z",
                author = "Marcus Weber",
                category = "Regulation",
                auditRelevance = 95,
                categoryScore = 8,
                matchedTerms = listOf("internal audit", "control deficiency", "control weakness", "enforcement", "supervision", "aml", "sanctions")
            ),
            AuditArticle(
                title = "Ransomware Infiltration of Banking SaaS Vendor Triggers Emergency Cyber Risk Audit at Major European Lenders",
                description = "Deutsche Bank, UBS, and BNP Paribas launch comprehensive technology risk evaluations after a critical cloud vendor reports unauthorized access and credential leakage.",
                content = "Chief Information Security Officers and IT Audit leads initiated vendor audit rights and digital forensics assessments. Preliminary internal control reviews confirmed customer data encryption remained intact, but highlighted third-party operational risk concentration.",
                url = "https://www.deutsche-bank.de/news",
                sourceName = "CyberScoop Finance",
                publishedAt = "2026-08-28T18:10:00Z",
                author = "Elena Rostova",
                category = "Cyber and Tech",
                auditRelevance = 85,
                categoryScore = 6,
                matchedTerms = listOf("it audit", "technology risk", "cybersecurity", "ransomware", "data breach", "internal controls")
            ),
            AuditArticle(
                title = "Citigroup Completes Remediation Milestone on Automated Ledger Controls Following Consent Order",
                description = "The banking giant delivers its second quarterly verification report to prudential regulators confirming the overhaul of risk data aggregation and reporting controls across corporate banking.",
                content = "External audit attestation confirmed substantial progress in replacing manual spreadsheet reconciliations with automated ledger controls. The Audit Committee affirmed that over 80% of legacy supervisory observations have been resolved.",
                url = "https://www.citigroup.com/citi/news",
                sourceName = "Wall Street Journal",
                publishedAt = "2026-08-27T10:00:00Z",
                author = "Robert Sterling",
                category = "Global Banks",
                auditRelevance = 70,
                categoryScore = 4,
                matchedTerms = listOf("audit committee", "external audit", "internal controls", "supervision", "governance")
            ),
            AuditArticle(
                title = "Barclays Deploys Agentic Workflow Automation in Risk Assurance and Continuous Internal Controls",
                description = "Modernizing 200-year-old banking inspection workflows, Barclays digital transformation teams partner with internal audit to cut sample validation cycle times from weeks to minutes.",
                content = "By applying autonomous verification agents to SOX compliance workflows, the bank enables continuous testing of segregation of duties, access management, and automated authorization thresholds across core banking ledgers.",
                url = "https://home.barclays/news",
                sourceName = "Banking Technology",
                publishedAt = "2026-08-26T15:00:00Z",
                author = "David Hall",
                category = "Transformation",
                auditRelevance = 75,
                categoryScore = 5,
                matchedTerms = listOf("internal controls", "automation", "core banking", "governance", "digital transformation")
            ),
            AuditArticle(
                title = "Morgan Stanley & Goldman Sachs Refresh Model Risk Governance Frameworks for Private Credit",
                description = "Investment banking audit committees approve elevated stress-testing requirements to address illiquid asset valuations and valuation control deficiencies.",
                content = "Internal audit teams will perform independent validation of proprietary discount curves and collateral adequacy metrics. The initiative aligns with recent Federal Reserve supervisory notices regarding private debt market interconnectedness.",
                url = "https://www.morganstanley.com/press-releases",
                sourceName = "Financial Review",
                publishedAt = "2026-08-25T12:00:00Z",
                author = "Jessica Vance",
                category = "People",
                auditRelevance = 65,
                categoryScore = 4,
                matchedTerms = listOf("audit committee", "model risk", "control deficiency", "governance", "risk management")
            ),
            AuditArticle(
                title = "Global Regulators Issue Joint Warning on Synthetic Identity Fraud and KYC Biometric Deficiencies",
                description = "Prudential and AML supervisors mandate enhanced synthetic fraud detection audits across mobile onboarding funnels for international banking groups.",
                content = "The advisory highlights deepfake bypasses of facial recognition gates during account origination. Bank internal audit functions are instructed to scrutinize fraud loss provisions, KYC exception approvals, and machine learning surveillance metrics.",
                url = "https://www.fincen.gov/news",
                sourceName = "FinTech Compliance Review",
                publishedAt = "2026-08-24T08:30:00Z",
                author = "Thomas Wright",
                category = "Cyber and Tech",
                auditRelevance = 80,
                categoryScore = 5,
                matchedTerms = listOf("internal audit", "financial crime", "fraud", "kyc", "aml", "compliance")
            )
        )
    }
}
