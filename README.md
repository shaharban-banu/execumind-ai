# ExecuMind AI

> **An AI-Powered Multi-Agent Executive Intelligence Platform for E-Commerce Decision Support**

ExecuMind AI is a dataset-agnostic, AI-driven executive intelligence platform that transforms raw e-commerce datasets into actionable business insights. The platform integrates intelligent data ingestion, AI agents, hybrid Retrieval-Augmented Generation (RAG), forecasting, and executive decision support to help business leaders make data-driven decisions.

---

## Executive Questions Answered

ExecuMind AI is designed to answer four key executive-level business questions:

- **What happened?** – Historical business analytics
- **Why did it happen?** – Customer intelligence using Hybrid RAG
- **What will happen?** – Time-series forecasting
- **What should we do?** – AI-generated executive recommendations

---

# Features

## Intelligent Dataset-Agnostic ETL

- Automatic dataset scanning
- Schema analysis
- Semantic table mapping
- Semantic column mapping
- Primary key detection
- Relationship detection
- Canonical schema generation
- Business capability detection
- Data transformation
- Data validation
- PostgreSQL loading

---

## AI Multi-Agent Architecture

### Data Intelligence Agent

Provides historical business analytics using SQL and MCP tools.

Capabilities include:

- Revenue Analysis
- Monthly Sales
- Customer Analytics
- Product Performance
- Seller Performance
- Payment Analysis
- Delivery Analysis

---

### Customer Intelligence Agent

Uses Hybrid RAG to answer customer intelligence questions.

Retrieval Pipeline:

- FAISS Vector Search
- BM25 Retrieval
- Reciprocal Rank Fusion (RRF)
- Cross-Encoder Re-ranking

Knowledge Sources:

- Customer Reviews
- Business Documents
- Research Reports

---

### Forecast Agent

Uses Facebook Prophet for forecasting.

Forecast Metrics:

- Revenue
- Orders
- Customers
- Average Order Value (AOV)

Model Evaluation:

- MAE
- RMSE
- MAPE

---

### Executive Agent

Combines outputs from:

- Data Intelligence Agent
- Customer Intelligence Agent
- Forecast Agent

Generates:

- Executive Summary
- Key Findings
- Business Risks
- Strategic Recommendations

---

# Dashboard

Interactive executive dashboard featuring:

- Revenue KPI
- Orders KPI
- Customers KPI
- Average Order Value
- Revenue Trend Chart
- Executive Briefing
- Platform Status
- Recent Activity Timeline

---

# Authentication

- JWT Authentication
- Login Page
- Protected API Endpoints
- Secure User Sessions

---

# Tech Stack

## Backend

- FastAPI
- Python 3.11
- SQLAlchemy ORM
- PostgreSQL
- Pydantic

## Frontend

- React
- TypeScript
- Tailwind CSS
- Axios

## AI & Machine Learning

- LangGraph
- LangChain
- FAISS
- Sentence Transformers
- Cross Encoder
- Prophet

## Database

- PostgreSQL

---

# System Architecture

```text
                    User
                      │
                      ▼
               React Frontend
                      │
                      ▼
               FastAPI Backend
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 Dataset ETL     AI Multi-Agent     Dashboard APIs
      │               │
      ▼               ▼
 PostgreSQL      LangGraph Workflow
                      │
      ┌───────────────┼───────────────────┐
      ▼               ▼                   ▼
Data Agent    Customer Agent      Forecast Agent
      │               │                   │
      ▼               ▼                   ▼
 SQL Tools      Hybrid RAG          Prophet Models
                      │
                      ▼
              Executive Agent
                      │
                      ▼
       Executive Recommendations
```

---

# Dataset Processing Pipeline

```text
Dataset Upload
      │
      ▼
Dataset Scanner
      │
      ▼
Schema Analyzer
      │
      ▼
Primary Key Detector
      │
      ▼
Semantic Mapper
      │
      ▼
Relationship Detector
      │
      ▼
Canonical Builder
      │
      ▼
Capability Detector
      │
      ▼
Transformer
      │
      ▼
Validator
      │
      ▼
PostgreSQL Loader
```

---

# Project Structure

```text
ExecuMind_AI/
│
├── app/                     # FastAPI application
├── database/                # Database configuration and ORM models
├── ingestion/               # Dataset-agnostic ETL pipeline
├── graph/                   # LangGraph workflow
├── agents/                  # AI agents
├── rag/                     # Hybrid RAG pipeline
├── forecast/                # Forecasting module
├── mcp/                     # SQL business tools
├── services/                # Business services
├── schemas/                 # Pydantic schemas
├── config/                  # Configuration
├── utils/                   # Utility functions
├── frontend/                # React frontend
├── tests/                   # Test suite
└── requirements.txt
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/<your-username>/ExecuMind_AI.git

cd ExecuMind_AI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/execumind

SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret

GROQ_API_KEY=your_groq_api_key

GOOGLE_API_KEY=your_google_api_key
```

---

# Initialize Database

```bash
python create_tables.py
```

---

# Run Backend

```bash
uvicorn app.main:app --reload
```

Backend Swagger UI:

```
http://localhost:8000/docs
```

---

# Run Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Platform Workflow

1. Login
2. Upload an e-commerce dataset
3. Process the platform
4. Train forecasting models
5. Build the Hybrid RAG knowledge base
6. Generate executive recommendations
7. Explore insights through the dashboard

---

# Key Highlights

- Dataset-Agnostic ETL
- Semantic Schema Mapping
- Automatic Relationship Detection
- Hybrid Retrieval-Augmented Generation (Hybrid RAG)
- Multi-Agent AI Architecture
- Prophet-based Forecasting
- Executive Decision Intelligence
- Interactive Dashboard
- JWT Authentication
- PostgreSQL Integration
- RESTful API

---

# Future Enhancements

- Docker deployment
- Cloud deployment (AWS/GCP/Azure)
- Role-Based Access Control (RBAC)
- Scheduled report generation
- Automated model retraining
- Real-time analytics
- Persistent vector database
- Monitoring and observability

---

# License

This project was developed as part of an academic capstone project for educational and research purposes.

---

# Author

**Banu**

**ExecuMind AI**  
*AI-Powered Multi-Agent Executive Intelligence Platform for E-Commerce Decision Support*