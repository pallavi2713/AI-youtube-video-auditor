#  BrandGuardian — YouTube Advertisement Compliance Auditor

> AI-powered compliance auditing for YouTube advertisements — detecting potential policy violations, misleading claims, and brand risks with evidence and timestamps.

---
Architecture:
<img width="1323" height="735" alt="image" src="https://github.com/user-attachments/assets/e8d1a2f4-541c-466c-84c3-19e6e403489e" />


##  Overview

BrandGuardian is an AI-powered video advertisement auditing system designed to analyze YouTube advertisements against configured compliance and brand guidelines.

Instead of manually reviewing an entire advertisement, BrandGuardian analyzes:

*  **Transcript**
*  **Visual/OCR content**
*  **Compliance rules**
*  **AI-generated analysis**

The system identifies potential compliance issues and produces a structured report containing the **violation category, severity, evidence, and timestamp**.

### Example

An advertisement containing:

> "Guaranteed results in 7 days"

could be flagged as:

```text
Category: Claim Validation
Severity: HIGH
Issue: Potentially misleading or unsupported claim
Evidence: "Guaranteed results in 7 days"
Timestamp: 00:14 - 00:18
```

---

## Problem Statement

Advertisement compliance is often a manual and time-consuming process.

Marketing and compliance teams need to review advertisements for:

* Misleading or exaggerated claims
* Unsupported guarantees
* Intellectual property concerns
* Brand guideline violations
* Regulatory or policy-specific risks

Reviewing video content manually can be difficult to scale.

**BrandGuardian automates the first layer of compliance review**, helping teams identify potential risks before an advertisement is published or during post-publication audits.

---

##  Key Features

###  YouTube Video Auditing

Submit a YouTube video URL and automatically process the advertisement.

###  Transcript Analysis

Extract spoken content from the video and analyze claims against configured compliance rules.

###  Visual & OCR Analysis

Analyze text appearing inside the video, including:

* Product claims
* Disclaimers
* Promotional text
* Brand names
* Logos

###  Compliance Issue Detection

Identify potential issues across configurable compliance categories.

Examples include:

* Claim Validation
* Misleading Claims
* Intellectual Property
* Brand Compliance
* Unsupported Statements
* Regulatory Compliance

###  Timestamped Evidence

Detected issues can contain evidence linked to the relevant section of the video.

```text
00:14 → 00:18
"Guaranteed results in 7 days"
```

###  Severity Classification

Each detected issue is assigned a severity level:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

###  AI-Powered Analysis

The system uses an LLM-based compliance workflow to analyze extracted video information and generate structured audit results.

### 📄 Structured Compliance Report

The final response contains:

* Overall compliance status
* Final report
* Issues detected
* Category
* Severity
* Evidence
* Timestamp

---

#  Architecture

```text
                    YouTube Advertisement
                              │
                              ▼
                         YouTube URL
                              │
                              ▼
                     Video Downloader
                              │
                              ▼
                    Azure Video Indexer
                         /          \
                        /            \
                       ▼              ▼
                 Transcript          OCR
                       │              │
                       └──────┬───────┘
                              ▼
                     Compliance Engine
                              │
                              ▼
                          LangGraph
                              │
                              ▼
                       Azure OpenAI
                              │
                              ▼
                    Compliance Analysis
                              │
                              ▼
                     Final Audit Report
                              │
                              ▼
                     Frontend Dashboard
```

---

#  Tech Stack

## Backend

* Python
* FastAPI
* LangGraph
* LangChain
* Pydantic
* yt-dlp

## AI & Azure

* Azure Video Indexer
* Azure OpenAI
* Azure AI Search
* Azure Identity
* Azure Application Insights

## Frontend

* Next.js
* React
* TypeScript

## Infrastructure

* Docker
* Azure Container Registry
* Azure Container Apps

---

#  Project Structure

```text
compliance_qa_pipeline/
│
├── backend/
│   └── src/
│       ├── api/
│       │   ├── server.py
│       │   └── telemetry.py
│       │
│       ├── graph/
│       │   ├── workflow.py
│       │   └── state.py
│       │
│       └── services/
│           └── video_indexer.py
│
├── frontend/
│   ├── app/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env.example
└── README.md
```

---

#  How It Works

## 1. Submit a YouTube Advertisement

Provide a YouTube URL through the frontend.

```text
https://www.youtube.com/watch?v=VIDEO_ID
```

---

## 2. Download the Video

The backend uses `yt-dlp` to retrieve the video for processing.

---

## 3. Video Indexing

The video is processed using **Azure Video Indexer**.

Video Indexer extracts information such as:

* Transcript
* OCR
* Video metadata
* Timing information

---

## 4. Compliance Analysis

The extracted information is passed into the LangGraph workflow.

The compliance agent evaluates the content against the configured compliance guidelines.

---

## 5. Generate Findings

Each potential issue is returned in a structured format.

Example:

```json
{
  "category": "Claim Validation",
  "severity": "HIGH",
  "evidence_type": "TRANSCRIPT",
  "evidence": "Guaranteed results in 7 days",
  "start_time": "00:14",
  "end_time": "00:18"
}
```

---

## 6. Display the Final Report

The frontend presents the audit result in a dashboard containing the overall report and individual compliance findings.

Example:

```text
FINAL COMPLIANCE REPORT

FAIL

2 potential compliance issues found


┌─────────────────────────────────────┐
│ Claim Validation             HIGH   │
│                                     │
│ "Guaranteed results in 7 days"      │
│                                     │
│ 00:14 ────────────────────── 00:18  │
└─────────────────────────────────────┘
```

---

# 🛠️ Local Setup

## Prerequisites

Make sure you have:

* Python 3.11+
* Node.js 18+
* Docker
* Azure subscription
* Azure Video Indexer
* Azure OpenAI
* Azure AI Search

---

# 🔐 Environment Variables

Create a `.env` file containing the required configuration.

Example:

```env
AZURE_SUBSCRIPTION_ID=
AZURE_RESOURCE_GROUP=

AZURE_VI_ACCOUNT_ID=
AZURE_VI_LOCATION=
AZURE_VI_NAME=

AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=
AZURE_OPENAI_CHAT_DEPLOYMENT=
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=

APPLICATIONINSIGHTS_CONNECTION_STRING=
```

> ⚠️ **Never commit `.env` or Azure credentials to GitHub.**

Use `.env.example` to document required environment variables without exposing secrets.

---

# ▶️ Running the Backend

Install dependencies using `uv`:

```bash
uv sync
```

Start the FastAPI server:

```bash
uv run uvicorn backend.src.api.server:app --host 0.0.0.0 --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

### Swagger Documentation

```text
http://localhost:8000/docs
```

### Health Check

```text
http://localhost:8000/health
```

---

# ▶️ Running the Frontend

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

---

#  Running with Docker

Build the Docker image:

```bash
docker build -t compliance-qa-pipeline .
```

Run the container:

```bash
docker run --env-file .env -p 8000:8000 compliance-qa-pipeline
```

The backend will be available at:

```text
http://localhost:8000
```

---

#  Azure Deployment

The backend can be containerized and deployed using **Azure Container Apps**.

High-level deployment flow:

```text
Local Application
       │
       ▼
Docker Build
       │
       ▼
Azure Container Registry
       │
       ▼
Azure Container Apps
       │
       ▼
Public API
       │
       ▼
Frontend
```

---

#  API

## POST `/audit`

Audits a YouTube advertisement.

### Request

```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

### Response

```json
{
  "session_id": "uuid",
  "video_id": "vid_12345678",
  "status": "FAIL",
  "final_report": "Potential compliance issues detected.",
  "compliance_results": [
    {
      "category": "Claim Validation",
      "severity": "HIGH",
      "evidence_type": "TRANSCRIPT",
      "evidence": "Guaranteed results in 7 days",
      "start_time": "00:14",
      "end_time": "00:18"
    }
  ]
}
```

---

#  Compliance Categories

The compliance engine can be configured to evaluate different categories.

| Category                  | Description                                   |
| ------------------------- | --------------------------------------------- |
| **Claim Validation**      | Detects unsupported or questionable claims    |
| **Misleading Claims**     | Identifies potentially deceptive statements   |
| **Intellectual Property** | Detects potential IP or brand-related issues  |
| **Brand Compliance**      | Checks content against configured brand rules |
| **Regulatory Compliance** | Checks applicable regulatory requirements     |

---

#  Evidence Types

The system can associate findings with different sources of evidence:

```text
TRANSCRIPT
VIDEO
TRANSCRIPT_AND_VIDEO
```

This allows reviewers to understand whether a potential issue was detected from spoken content, visual content, or both.

---

#  Example Audit Result

```text
Status: FAIL

Final Report:
Potential compliance issues detected.

Issues:

1. Claim Validation
   Severity: HIGH

   Evidence:
   "Guaranteed results in 7 days"

   Evidence Type:
   TRANSCRIPT

   Timestamp:
   00:14 - 00:18


2. Brand Compliance
   Severity: MEDIUM

   Evidence:
   Promotional text detected in video.

   Evidence Type:
   VIDEO

   Timestamp:
   00:32 - 00:36
```

---

#  Security

Sensitive credentials should be supplied through environment variables or managed Azure identity mechanisms.

Do not commit:

```text
.env
API keys
Azure credentials
Access tokens
Secrets
```

The `.gitignore` file should exclude sensitive configuration files.

---

#  Important Disclaimer

BrandGuardian is an **AI-assisted compliance auditing tool**.

A detected issue represents a **potential compliance risk**, not a definitive legal determination or official platform enforcement decision.

The final decision should be made by an appropriate compliance, legal, or policy team.

---

#  Project

## BrandGuardian — YouTube Advertisement Compliance Auditor

Built with:

**Python · FastAPI · LangGraph · LangChain · Azure AI · Next.js · Docker**

---

## 📌 Note on Compliance Guidelines

BrandGuardian is designed to evaluate advertisements against **configured compliance guidelines**.

The system should only be described as checking specific platform policies, regulatory requirements, or official advertising guidelines when those rules are actually included in the project's compliance knowledge base or configuration.

This keeps the audit results technically accurate and avoids implying that the system provides an official platform or legal compliance determination.
