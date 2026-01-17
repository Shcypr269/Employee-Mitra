# Employee-Mitra

*(Hackathon Variant: **HCLTech Agentic Enterprise Assistant**)*

---

## 📚 Table of Contents

- Overview  
- Problem Statement  
- Why This Project Stands Out  
- Key Features  
- Traditional RAG vs Agentic RAG  
- System Architecture  
- Tech Stack  
- How It Works  
- Quick Demo  
- API Endpoints Table  
- API Usage Example  
- Configuration (Environment Variables)  
- Running Locally  
- Deployment Strategy  
- Security Considerations  
- Performance & Scalability Notes  
- Development & Extensibility  
- Troubleshooting  
- Future Enhancements  
- Hackathon Note  
- Contributing  
- License  
- Team / Credits  

---

## Overview

The **Agentic Enterprise Assistant** is an enterprise-focused NLP system designed to go beyond traditional chatbots by combining:

- 📄 **Document-grounded Q&A using RAG**
- 🧠 **Agentic intent detection**
- ⚙️ **Enterprise action execution via structured JSON outputs**

It enables employees to:

- Ask factual questions from internal PDFs (e.g., annual reports, policies, SOPs)
- Receive page-level citations for traceability
- Trigger enterprise workflows through natural language

This system demonstrates how **Agentic RAG** can bridge the gap between knowledge retrieval and operational automation in enterprise environments.

---

## Problem Statement

Enterprises face two major challenges with AI assistants:

### Hallucination Risk

Traditional chatbots may generate confident but incorrect responses without grounding in enterprise data.

### Lack of Operational Capability

Most systems can answer questions but cannot trigger real enterprise actions like:

- Leave requests  
- IT tickets  
- Meeting scheduling  

As a result, employees still rely on fragmented portals and manual processes.

---

## Why This Project Stands Out

- ✅ Combines **RAG + Agentic reasoning**
- ✅ Produces **hallucination-safe answers with citations**
- ✅ Detects **user intent with confidence scoring**
- ✅ Outputs **structured JSON for enterprise automation**
- ✅ Designed with **enterprise workflows in mind**
- ✅ Clean **API-first architecture** for easy integration

💡 This project is not just a chatbot — it is a **decision-making assistant with execution capability**.

---

## Key Features

### 📄 Document Intelligence

- PDF ingestion pipeline
- Chunk-based retrieval with metadata
- Page-level citations

### 🧠 Agentic Reasoning

- Intent classification (Q&A vs Action)
- Confidence scoring
- Routing logic

### ⚙️ Enterprise Actions (Mock Integrations)

Supported actions include:

- `apply_leave`
- `schedule_meeting`
- `file_ticket`
- `request_software`
- `escalate_issue`
- `update_documentation`

⚠️ **Note:** Actions are executed via mock/stub handlers for hackathon demonstration. No real enterprise systems are connected.

### 🔐 Enterprise-Ready Design

- Environment-based configuration
- Dockerized deployment
- API-first design

---

## Traditional RAG vs Agentic RAG

| Feature | Traditional RAG | Agentic RAG (This Project) |
|--------|------------------|----------------------------|
| Document grounding | ✅ Yes | ✅ Yes |
| Citations | ⚠️ Optional | ✅ Mandatory |
| Intent detection | ❌ No | ✅ Yes |
| Action execution | ❌ No | ✅ Yes |
| Structured outputs | ❌ No | ✅ JSON schemas |
| Workflow automation | ❌ Not supported | ✅ Supported |
| Enterprise use cases | Limited | Strong fit |

---

## System Architecture

### Textual Flow

1. User sends query  
2. Agent layer evaluates intent  
3. If factual → RAG retrieval  
4. If operational → action routing  
5. LLM generates grounded response or structured JSON  
6. Final response returned with citations or action result  

### ASCII Architecture Diagram

User
│
▼
Agent Layer
│
├── Intent Detector
│
├── RAG Retriever (FAISS)
│
└── Action Executor (JSON)
│
▼
LLM (Groq / Claude / GPT)
│
▼
Final Response + Citations / Action JSON

yaml
Copy code

---

## Tech Stack

| Category | Technology |
|--------|------------|
| Language | Python 3.10 / 3.11 / 3.12 |
| Backend | FastAPI, Uvicorn |
| Agent Framework | LangChain (lightweight usage) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| PDF Parsing | PyPDF2 |
| LLM API | Groq (LLaMA 3) |
| Containerization | Docker |
| Hosting | Hugging Face Spaces |
| Dev Tunneling | ngrok (development only) |
| Secrets Management | Environment variables |

---

## How It Works

### Step-by-Step Flow

#### 1. PDF Ingestion

- PDFs are parsed using PyPDF2  
- Text is chunked (~1000 chars, 200 overlap)  
- Embeddings are generated  
- Stored in FAISS vector index with page metadata  

#### 2. User Query Received

- Query sent to FastAPI endpoint  

#### 3. Intent Detection

- Keyword + scoring-based intent classifier  
- Determines:
  - Q&A intent
  - Action intent
  - Ambiguous (fallback to Q&A)

#### 4. Routing Logic

- If Q&A → Vector retrieval  
- If Action → Action schema selected  

#### 5. LLM Processing

- LLM receives:
  - Retrieved context (for RAG)
  - Or action schema (for structured output)

#### 6. Response Generation

- Factual answers include:
  - Extracted answer
  - Source page numbers  
- Actions return:
  - JSON with required parameters

#### 7. Action Execution (Mock)

- Action handler simulates enterprise response

---

## Quick Demo

### Example Q&A Queries

- “What is the revenue mentioned in the annual report?”  
- “Summarize employee benefits policy.”  
- “Which page talks about sustainability initiatives?”  

### Example Action Queries

- “Apply leave for next Monday.”  
- “Schedule a meeting with IT team tomorrow at 11.”  
- “Raise a ticket for VPN access issue.”  
- “Request Photoshop software.”  

---

## API Endpoints Table

| Method | Endpoint | Description | Example |
|--------|--------|------------|--------|
| POST | `/query` | Unified endpoint for Q&A and Actions | Natural language query |
| POST | `/action` | Direct action execution | JSON payload |
| GET | `/health` | Service health check | Returns status |

---

## API Usage Example

### ✅ Q&A Request

#### Request

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is mentioned about cloud services in the report?"
  }'
Response
json
Copy code
{
  "type": "qa",
  "answer": "The report highlights expansion of cloud-native solutions and enterprise cloud modernization services.",
  "citations": [
    {
      "page": 42,
      "source": "Annual_Report_2024.pdf"
    }
  ],
  "confidence": 0.87
}
⚙️ Action Request
Request
bash
Copy code
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Apply leave for tomorrow due to medical reason"
  }'
Response
json
Copy code
{
  "type": "action",
  "action": "apply_leave",
  "parameters": {
    "date": "2025-01-18",
    "reason": "medical"
  },
  "status": "mock_executed",
  "message": "Leave request submitted successfully (mock)."
}
Configuration (Environment Variables)
Create a .env file or export variables:

env
Copy code
LLM_PROVIDER=groq
GROQ_API_KEY=your_real_key_here
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DB_PATH=vectorstore/
PDF_DATA_PATH=data/
APP_HOST=0.0.0.0
APP_PORT=8000
⚠️ Note: Never commit .env files to version control.

Running Locally
1. Clone Repository
bash
Copy code
git clone <repository>
cd project
2. Install Dependencies
bash
Copy code
pip install -r requirements.txt
3. Ingest PDFs (Optional)
bash
Copy code
python ingest.py
4. Start API Server
bash
Copy code
uvicorn app:app --host 0.0.0.0 --port 8000
5. Test API
Send requests to:

bash
Copy code
http://localhost:8000/query
💡 Tip: Use ngrok only during development if exposing local server for demos.

Deployment Strategy
✅ Recommended: Hugging Face Spaces
Docker-based deployment

Prebuilt FAISS index included

Stateless API with persistent vectorstore

Docker Deployment
bash
Copy code
docker build -t agentic-assistant .
docker run -p 8000:8000 agentic-assistant
Environment Setup
Set secrets via platform environment variables

Avoid embedding keys in images

⚠️ ngrok is for development only. Not used in final deployment.

Security Considerations
API keys stored only in environment variables

No hardcoded secrets

No persistent user data stored

PDF data assumed to be non-sensitive demo documents

Production deployment should include:

Authentication

Role-based access control

Audit logging

Performance & Scalability Notes
FAISS enables fast similarity search for medium-scale datasets

Embedding generation happens only during ingestion

Stateless API allows horizontal scaling

Bottlenecks
LLM API latency

Large PDF ingestion time

✅ Suitable for:

Hackathon demos

Internal POCs

Pilot enterprise assistants

Development & Extensibility
Add New Actions
Define JSON schema in actions.py

Add handler function

Register in agent router

Swap LLM Provider
Modify llm_handler.py or config

Supported patterns:

Groq

OpenAI

Anthropic

Add UI
Optional Streamlit frontend can be added for:

Chat interface

File upload

Action visualization

Troubleshooting
FAISS Index Not Found
pgsql
Copy code
Error: Vectorstore path not found
✅ Solution: Run ingest.py before starting server.

LLM API Errors
mathematica
Copy code
Authentication failed
✅ Solution: Verify API key in environment variables.

PDF Parsing Issues
arduino
Copy code
Empty text extracted
✅ Solution:

Check PDF is text-based

Avoid scanned image PDFs without OCR

Future Enhancements
🔐 Authentication & role-based access

🧩 Plugin-based action framework

📊 Analytics dashboard

🧠 Learning-based intent detection

📎 Multi-document knowledge bases

🔄 Workflow orchestration integration

📥 Upload PDFs via API/UI

Hackathon Note
This project was developed as part of the:

NLP Challenge — HCLTech AI Hackathon 2025

Focus areas:

Enterprise AI

Responsible RAG

Agentic workflows

Practical business automation

All enterprise actions are mock implementations designed for demonstration only.

Contributing
Contributions are welcome.

Suggested improvements:

Better intent classification

Additional action handlers

UI enhancements

Evaluation metrics

Contribution Flow
Fork repository

Create feature branch

Commit changes

Submit pull request

License
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

Team / Credits
Team Name: Hackathon Team Placeholder

Roles
AI Engineer

Backend Developer

ML Engineer

Product Designer

Acknowledgements
Open-source NLP community

Sentence-Transformers

FAISS contributors

FastAPI ecosystem
