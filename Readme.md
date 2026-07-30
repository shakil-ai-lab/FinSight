# 📊 FinSight

> **AI-Powered Financial Statement Analysis & Investment Decision Support**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-LLM_Framework-blueviolet.svg)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Workflow-orange.svg)](https://www.langchain.com/langgraph)
[![Google Gemini](https://img.shields.io/badge/LLM-Google_Gemini-4285F4.svg)](https://ai.google.dev/)
[![Railway](https://img.shields.io/badge/Deployment-Railway-purple.svg)](https://railway.app/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)](#license)

---

## 📖 Overview

**FinSight** is an AI-powered financial statement analysis platform that automatically analyzes SEC filings and earnings call transcripts to generate structured financial insights and explainable investment recommendations.

Instead of manually reading hundreds of pages of financial reports, users can obtain an AI-generated analyst brief containing financial metrics, business performance, management insights, risk assessment, and an investment recommendation through an interactive dashboard.

This project was developed as part of an **MS Data Science portfolio** to demonstrate the practical application of:

- Artificial Intelligence
- Large Language Models (LLMs)
- Financial Statement Analysis
- Natural Language Processing (NLP)
- Clean Architecture
- Domain-Driven Design
- Agentic AI Workflows

---

# 🎯 Project Objectives

Traditional financial statement analysis is time-consuming and requires extensive domain expertise.

FinSight aims to automate this process by:

- Acquiring SEC filings automatically
- Parsing financial documents
- Extracting structured financial knowledge using LLMs
- Performing financial and qualitative analysis
- Assessing business risks
- Generating explainable investment recommendations
- Presenting insights through an interactive dashboard

---

# ✨ Features

### 📑 Financial Document Processing

- SEC Filing Acquisition
- Earnings Call Transcript Processing
- Intelligent Document Parsing

### 🤖 AI Knowledge Extraction

- Financial Snapshot Extraction
- Business Segment Analysis
- Management Discussion Extraction
- Guidance Summary
- Earnings Call Analysis

### 📈 Financial Analysis

- Executive Summary
- Financial Snapshot
- Revenue Analysis
- Profitability Analysis
- Cash Flow Analysis
- Business Segment Performance

### ⚠️ Risk Intelligence

- Risk Assessment
- Key Risks
- Communication Analysis
- Consistency Analysis
- Materiality Assessment
- Trend Analysis

### 💼 Investment Decision Support

- BUY / HOLD / SELL Recommendation
- Confidence Score
- Investment Rationale
- Executive Brief

### 🖥 Dashboard

- Modern Streamlit Dashboard
- Interactive User Interface
- Financial Metrics Visualization
- Explainable AI Output

---

# 📷 Dashboard Preview

## 🏠 Investment Recommendation

![Home](assets/home_snapshot.png)

The dashboard provides an explainable investment recommendation together with a confidence score and investment rationale.

---

## 💰 Financial Snapshot

![Financial Snapshot](assets/financial_snapshot.png)

Displays the company's key financial indicators, including:

- Revenue
- Net Income
- Operating Cash Flow
- Diluted EPS

---

## 🌍 Business Segment Analysis

![Business Segment](assets/business_segment.png)

Provides a geographical revenue breakdown together with growth analysis for each business segment.

---

# 🏗 System Architecture

FinSight follows **Clean Architecture** and **Domain-Driven Design (DDD)** to keep business logic independent from frameworks and external services.

```
                    Presentation Layer
                     (Streamlit UI)
                            │
                            ▼
                  Application Layer
          (Use Cases & Business Services)
                            │
                            ▼
                     Domain Layer
            (Business Models & Rules)
                            │
                            ▼
                Infrastructure Layer
      (Gemini, SEC API, Database, Parsing)
```

This architecture ensures:

- Separation of concerns
- Loose coupling
- High maintainability
- Testability
- Easy replacement of external services
- Better scalability

---

# 🧠 Software Engineering Principles

The project follows modern software engineering practices.

| Principle | Purpose |
|------------|----------|
| Clean Architecture | Separates business logic from infrastructure |
| Domain-Driven Design (DDD) | Models real-world financial concepts |
| SOLID Principles | Produces maintainable and extensible software |
| Dependency Inversion Principle | Business logic depends on abstractions instead of implementations |
| Port & Adapter Pattern | Makes external services easily replaceable |
| Dependency Injection | Reduces coupling between components |

---

# 🤖 AI Analysis Workflow

FinSight performs financial analysis using a multi-stage AI pipeline.

```
                     User Request
                           │
                           ▼
                  Planning Capability
                           │
                           ▼
               Document Acquisition
                           │
                           ▼
                  Document Parsing
                           │
                           ▼
                Knowledge Extraction
                           │
                           ▼
                 Knowledge Analysis
                           │
                           ▼
                Decision Support Engine
                           │
                           ▼
                Presentation Generation
                           │
                           ▼
                  Streamlit Dashboard
```

Each capability performs a single responsibility, making the system modular, explainable, and maintainable.

---

# 📋 Dashboard Outputs

After analyzing a company, FinSight generates:

- ✅ Investment Recommendation
- ✅ Confidence Score
- ✅ Investment Rationale
- ✅ Executive Summary
- ✅ Financial Snapshot
- ✅ Business Segment Analysis
- ✅ Management Discussion
- ✅ Guidance Summary
- ✅ Risk Assessment
- ✅ Key Risks
- ✅ Trend Analysis
- ✅ Quarter Comparison
- ✅ Consistency Analysis
- ✅ Communication Analysis
- ✅ Materiality Assessment
- ✅ Executive Analyst Brief

These outputs transform lengthy financial reports into actionable insights that support investment decision-making.

---