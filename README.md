# ⚡ Speed-to-Lead: Inbound Lead Qualifier & Executive Slack Engine

> **Autonomous inbound revenue infrastructure in Python.** Intercepts B2B demo requests, extracts real-time company metadata in milliseconds, classifies enterprise ICP tiers with LLM orchestration, and dispatches rich Slack Block Kit dossiers to sales reps before the prospect closes their browser tab.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Slack Block Kit](https://img.shields.io/badge/Slack-Block_Kit-4A154B?style=flat-square&logo=slack&logoColor=white)](https://api.slack.com/block-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## 🎯 The Business Problem: Why "Speed-to-Lead" Matters

In enterprise B2B sales, inbound demo requests have an extremely aggressive decay curve:
* **The 5-Minute Window:** Research published by *Harvard Business Review* and *Chili Piper* demonstrates that **responding to an inbound lead within 5 minutes makes them 21x more likely to enter the sales pipeline** compared to waiting 30 minutes.
* **The Manual Friction:** Most sales teams take hours or days to respond because sales reps must manually look up the prospect on LinkedIn, inspect their company website, evaluate company size, and write an account briefing note.
* **The Competitor Cost:** Enterprise platforms like **Chili Piper**, **Qualified**, and custom revenue routers charge SaaS companies anywhere from **$30,000 to $60,000 every year** to automate this workflow.

This project implements an open-source, production-grade inbound revenue pipeline using **Anthropic Enterprise** as the anchor business use case.

---

## 🏗️ System Architecture

```
[ Web Demo Form Submission ] ── (HubSpot, Marketo, or Next.js Frontend)
              │
              ▼
    [ FastAPI Webhook ]        ── Ingests & validates payload via Pydantic v2
              │
              ├── [ Personal Email? ] ──► (YES) ──► Fast-Fail: Auto-Disqualify (0.0s, 0 tokens)
              │
              ▼ (NO)
   [ Real-Time Web Crawler ]   ── Extracts homepage title, meta description & H1s (< 1s)
              │
              ▼
    [ AI ICP Triage Engine ]   ── Evaluates Anthropic Enterprise ICP criteria (Tier A / B / C / DQ)
              │
              ▼
   [ Slack Block Kit Engine ]  ── Formats executive dossier (30-second AE cheat sheet)
              │
              ▼
  [ Real-Time Alert Dispatch ] ── Posts directly to #inbound-sales-alerts Slack channel
```

---

## 📐 The 4-Tier Qualification Rubric (Anthropic Enterprise Case Study)

The engine evaluates incoming leads against Anthropic Enterprise criteria ($30k–$100k+ commitments for Claude Enterprise & Provisioned Throughput):

| Tier | Target Profile | Key Signals & Pain Points | Automated Action |
| :--- | :--- | :--- | :--- |
| **Tier A** | Enterprise / High Priority | 50+ employees or known B2B brands; production rate-limit bottlenecks (429 errors), enterprise compliance mandates (ZDR, HIPAA, SOC2). | `🚨 Immediate Slack Alert & Route to Enterprise AE` |
| **Tier B** | Mid-Market / Growth | 10–50 employees; funded tech startups integrating Claude into core products; custom volume pricing or SLA inquiries. | `📅 Fast-Track: Automated calendar booking link` |
| **Tier C** | SMB / Prototyping | 1–10 employees; solo devs or early experiments with low initial volume. | `📩 Product-Led: Route to Developer Console & pay-as-you-go tiers` |
| **Disqualified** | Non-Commercial / Spam | Personal emails (`@gmail.com`, `@yahoo.com`), students, job seekers, or vendor solicitation spam. | `🚫 Disqualify: Archive without notifying sales reps` |

---

## 📊 Benchmark Test Suite: 100% Precision Across All Tiers

An automated test suite (`test_suite.py`) verifies the entire pipeline end-to-end across realistic enterprise, mid-market, SMB, personal email, and spam payloads:

```text
================================================================================
📊 EXECUTIVE BENCHMARK SUMMARY
================================================================================
Company         | Email                        | Expected     | Actual       | Latency  | Status
--------------------------------------------------------------------------------
Linear          | sarah.chen@linear.app        | Tier A       | Tier A       | 17.13s   | ✅ PASS
Resend          | david@resend.com             | Tier B       | Tier B       | 17.06s   | ✅ PASS
TinyCraft       | marcus@tinycraft.dev         | Tier C       | Tier C       | 15.64s   | ✅ PASS
Self            | alex.reynolds99@gmail.com    | Disqualified | Disqualified | 0.0s     | ✅ PASS
TokenBlast      | promo@tokenblast-xyz.io      | Disqualified | Disqualified | 16.05s   | ✅ PASS
================================================================================
```

### ⚡ Deterministic Fast-Fail
Notice that `alex.reynolds99@gmail.com` resolved in **0.00 seconds**. By enforcing deterministic business email verification (`is_business_email`) in code before invoking the LLM, the system saves thousands of dollars in unnecessary LLM inference costs and eliminates latency for spam.

---

## 💬 The Sales Rep Slack Dossier (Block Kit)

When an enterprise lead arrives, Account Executives receive a formatted dossier in Slack with a **30-second cheat sheet** summarizing the company and the exact operational pain point:

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚨 [TIER A] Inbound Lead: Sarah Chen @ Linear"
      }
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*Company:*\nLinear (linear.app)"},
        {"type": "mrkdwn", "text": "*Contact:*\nSarah Chen (<mailto:sarah.chen@linear.app|sarah.chen@linear.app>)"},
        {"type": "mrkdwn", "text": "*Company Size:*\n50-200"},
        {"type": "mrkdwn", "text": "*Evaluation Confidence:*\nHigh"}
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*🏢 Company Overview:*\nLinear is a leading product development and issue tracking system built for modern engineering teams and autonomous AI agents."
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*⚡ Technical Bottleneck (AE Cheat Sheet):*\nHitting 429 rate-limit bottlenecks in production while deploying user-facing AI agents for issue tracking, requiring dedicated throughput (provisioned TPM) and Zero Data Retention (ZDR)."
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*🎯 Recommended Next Action:*\n🚨 Priority Route: Immediate Slack Alert & Assign to Enterprise AE"
      }
    }
  ]
}
```

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Sameer330/speed-to-lead-engine.git
cd speed-to-lead-engine
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Automated Test Suite
```bash
python3 test_suite.py
```

### 4. Start the Live FastAPI Webhook Server
```bash
uvicorn app:app --reload --port 8000
```

### 5. Send a Live Test Webhook Request
```bash
curl -X POST http://127.0.0.1:8000/webhook/inbound-lead \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Sarah",
    "last_name": "Chen",
    "email": "sarah.chen@linear.app",
    "company_name": "Linear",
    "company_domain": "linear.app",
    "company_size": "50-200",
    "use_case": "We are rolling out AI agents across Linear for issue tracking. Hitting 429 rate limits in production. Need dedicated throughput (provisioned TPM) and enterprise ZDR."
  }'
```

---

## 🛠️ Tech Stack

* **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) (High-performance async ASGI server)
* **Data Contracts & Validation:** [Pydantic v2](https://docs.pydantic.dev/)
* **Web Scraping:** [HTTPX](https://www.python-httpx.org/) + [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* **AI Orchestration:** Spec-Driven Prompt Contracts + Local/Cloud LLMs
* **Alerting:** [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks) & [Block Kit Builder](https://app.slack.com/block-kit-builder)

---

## 💼 Work With Me

I am a Software Engineer specializing in **Go-To-Market (GTM) Engineering, Signal-Based Outbound Systems, and Inbound Revenue Infrastructure**.

If your startup or revenue team is looking to automate lead triage, enrich prospects in real time, or turn developer/hiring intent into pipeline, I am available for **full-time engineering roles, contract projects, and advisory work**.

* 🔗 **LinkedIn:** [linkedin.com/in/sameer-ankalagi](https://www.linkedin.com/in/sameer-ankalagi)
* 📧 **Email:** [330.sameer@gmail.com](mailto:330.sameer@gmail.com)
* 💻 **GitHub:** [@Sameer330](https://github.com/Sameer330)
