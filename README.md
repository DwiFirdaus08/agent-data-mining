<div align="center">

# 🤖 Agent Data Mining

### Autonomous Data Mining Microservice for Multi-Agent AI System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)

<br/>

**Agent Data Mining** is one of **22 specialized autonomous agents** in the **Joki Tugas AI** multi-agent orchestration system. This agent is responsible for performing real-time data mining, pattern extraction, and machine learning analysis on incoming datasets — all through a single REST API endpoint.

[Live Demo](https://agent-data-mining-production.up.railway.app/docs) · [API Contract](#-api-contract) · [Architecture](#-architecture)

</div>

---

## 📋 Table of Contents

- [Highlights](#-highlights)
- [Architecture](#-architecture)
- [Machine Learning Algorithms](#-machine-learning-algorithms)
- [Tech Stack](#-tech-stack)
- [API Contract](#-api-contract)
- [Getting Started](#-getting-started)
- [Deployment](#-deployment)
- [Multi-Agent Integration](#-multi-agent-integration)
- [Project Structure](#-project-structure)

---

##  Highlights

| Feature | Description |
|:---|:---|
|  **4 ML Algorithms** | K-Means Clustering, Linear Regression, Decision Tree Classification, Correlation Analysis |
|  **Plug & Play** | Standardized API contract — orchestrator auto-discovers and communicates with this agent |
|  **Smart Input Handling** | Accepts raw text, CSV data, or remote dataset URLs for flexible data ingestion |
| **Pipeline Compatible** | Designed for Type-Safe Smart Skip — seamlessly chains with 21 other agents in the pipeline |
|  **Containerized** | Fully Dockerized with production-ready deployment on Railway |
| **Auto-documented** | Interactive Swagger UI at `/docs` for instant API testing |

---

##  Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR                          │
│            jokitugas.bananaunion.web.id                 │
└──────────────────────┬──────────────────────────────────┘
                       │  HTTP POST /process
                       ▼
┌─────────────────────────────────────────────────────────┐
│              AGENT DATA MINING                          │
│                                                         │
│  ┌─────────┐    ┌──────────┐    ┌───────────────────┐  │
│  │ Router  │───▶│ Schemas  │───▶│  Mining Service    │  │
│  │ /process│    │ Validate │    │                    │  │
│  └─────────┘    └──────────┘    │  ┌──────────────┐  │  │
│                                 │  │  K-Means     │  │  │
│                                 │  │  Regression  │  │  │
│                                 │  │  Dec. Tree   │  │  │
│                                 │  │  Correlation │  │  │
│                                 │  └──────────────┘  │  │
│                                 └───────────────────┘  │
└─────────────────────────────────────────────────────────┘
                       │
                       ▼  JSON Response
┌─────────────────────────────────────────────────────────┐
│          NEXT AGENT IN PIPELINE                         │
│     (summarizer / ppt_generator / etc.)                 │
└─────────────────────────────────────────────────────────┘
```

---

##  Machine Learning Algorithms

This agent dynamically selects the appropriate algorithm based on the `keyword` parameter and the structure of the input data:

### 1. K-Means Clustering
> **Trigger keyword:** `cluster`, `kelompok`

Performs unsupervised learning to group dataset rows into **3 distinct clusters** based on numerical features. Useful for customer segmentation, anomaly grouping, and pattern discovery.

### 2. Linear Regression
> **Trigger keyword:** `regresi`, `prediksi`

Builds a supervised regression model to predict continuous numerical values. Returns the **R-Squared accuracy score** indicating model reliability.

### 3. Decision Tree Classification
> **Trigger keyword:** `klasifikasi`, `label`

Constructs a decision tree (max depth 3) to classify categorical labels based on numerical input features. Ideal for pass/fail predictions and category assignment.

### 4. Correlation & Association Analysis
> **Trigger keyword:** `asosiasi`, `pola`, `korelasi`

Computes Pearson correlation matrix across all numerical columns and identifies the **strongest feature relationships** (>50% correlation).

### 5. Automated Data Profiling *(Default Fallback)*
When no specific keyword is provided, the agent performs a comprehensive data profiling — reporting row/column counts, averages, and max values for immediate statistical insight.

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Framework** | FastAPI | High-performance async REST API |
| **ML Engine** | scikit-learn | Machine learning algorithms |
| **Data Processing** | Pandas | Dataset parsing, cleaning, and transformation |
| **Validation** | Pydantic | Request/response schema validation |
| **Server** | Uvicorn | ASGI production server |
| **Container** | Docker | Reproducible deployment environment |
| **Hosting** | Railway | Cloud deployment with auto-scaling |

---

##  API Contract

### Endpoint
```
POST /process
```

### Request Body
```json
{
  "task_id": "req-12345-abc",
  "agent_type": "data_mining",
  "payload": {
    "url": "https://example.com/dataset.csv",
    "keyword": "cluster",
    "raw_text": ""
  },
  "metadata": {
    "sender": "orchestrator",
    "timestamp": 1689694097
  }
}
```

| Field | Type | Description |
|:---|:---|:---|
| `task_id` | `string` | Unique task identifier — returned as-is in response |
| `agent_type` | `string` | Agent identifier (`data_mining`) |
| `payload.url` | `string` | URL to a remote CSV dataset |
| `payload.keyword` | `string` | ML algorithm trigger (`cluster` / `regresi` / `klasifikasi` / `korelasi`) |
| `payload.raw_text` | `string` | Raw text or CSV string from a previous agent's output |
| `metadata` | `object` | Sender info and Unix timestamp |

### Success Response `200 OK`
```json
{
  "status": "success",
  "task_id": "req-12345-abc",
  "data": {
    "result": "Proses Clustering (K-Means) selesai. Dataset (150 baris) berhasil dikelompokkan menjadi 3 klaster utama.",
    "file_url": null
  },
  "message": "Pemrosesan Data Mining berhasil"
}
```

### Error Response `500`
```json
{
  "status": "error",
  "task_id": "req-12345-abc",
  "data": null,
  "message": "Internal Server Error: detail error message"
}
```

---

##  Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/agent-data-mining.git
cd agent-data-mining

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 7860
```

### Test the API

```bash
curl -X POST http://localhost:7860/process \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test-001",
    "agent_type": "data_mining",
    "payload": {
      "url": "",
      "keyword": "cluster",
      "raw_text": "name,score,grade\nAlice,85,A\nBob,72,B\nCharlie,91,A"
    },
    "metadata": { "sender": "orchestrator", "timestamp": 1689694097 }
  }'
```

Or visit the interactive docs at: **http://localhost:7860/docs**

---

## 🐳 Deployment

### Docker

```bash
# Build
docker build -t agent-data-mining .

# Run
docker run -p 7860:7860 agent-data-mining
```

### Railway (Production)

This agent is deployed on **Railway** with automatic builds from Git push:

```
🌐 Live: https://agent-data-mining-production.up.railway.app
📖 Docs: https://agent-data-mining-production.up.railway.app/docs
```

---

## 🔗 Multi-Agent Integration

This agent operates as part of a **22-agent orchestration pipeline** managed by a central orchestrator. The system implements a **Type-Safe Smart Skip** mechanism for fault tolerance.

### Data Flow Compatibility

```
Input Type  : text | url
Output Type : text
```

### Pipeline Examples

```
web_scraper → data_mining → summarizer → ppt_generator
                  ▲
                  │ You are here
```

```
web_scraper → data_mining → outliner → translator
```

---

## 📁 Project Structure

```
agent-data-mining/
├── main.py                  # FastAPI app entry point & CORS config
├── routers/
│   └── analyze.py           # POST /process endpoint handler
├── schemas/
│   └── payload.py           # Pydantic request/response models
├── services/
│   └── mining_service.py    # ML engine (4 algorithms + profiling)
├── Dockerfile               # Container build configuration
├── requirements.txt         # Python dependencies
├── .dockerignore             # Docker build exclusions
└── README.md
```

---

## 👥 Team

Developed as part of the **Joki Tugas AI: Multi-Agent System** — a collaborative final project for the **Artificial Intelligence** course (Semester 6), Div TI 3B 2026.

---

<div align="center">

**Built with  using FastAPI + scikit-learn**

</div>
