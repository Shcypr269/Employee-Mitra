# Employee-Mitra

## Table of Contents

- Overview  
- Problem Statement  
- Why This Project Stands Out  
- Key Features 
- System Architecture  
- Tech Stack  
- How It Works  
- Quick Demo  


## Overview

The **Agentic Enterprise Assistant** is an enterprise-focused NLP system designed to go beyond traditional chatbots by combining:

- **Document-grounded Q&A using RAG**
- **Agentic intent detection**
- **Enterprise action execution via structured JSON outputs**

It enables employees to:

- Ask factual questions from internal PDFs (e.g., annual reports, policies, SOPs)
- Receive page-level citations for traceability
- Trigger enterprise workflows through natural language

This system demonstrates how **Agentic RAG** can bridge the gap between knowledge retrieval and operational automation in enterprise environments.

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

## Why This Project Stands Out

- Combines **RAG + Agentic reasoning**
- Produces **hallucination-safe answers with citations**
- Detects **user intent with confidence scoring**
- Outputs **structured JSON for enterprise automation**
- Designed with **enterprise workflows in mind**
- Clean **API-first architecture** for easy integration

This project is not just a chatbot — it is a **decision-making assistant with execution capability**.

## Key Features

### Document Intelligence

- PDF ingestion pipeline
- Chunk-based retrieval with metadata
- Page-level citations

### Agentic Reasoning

- Intent classification (Q&A vs Action)
- Confidence scoring
- Routing logic

### Enterprise Actions (Mock Integrations)

Supported actions include:

- `apply_leave`
- `schedule_meeting`
- `file_ticket`
- `request_software`
- `escalate_issue`
- `update_documentation`

**Note:** Actions are executed via mock/stub handlers for hackathon demonstration. No real enterprise systems are connected.

### Enterprise-Ready Design

- Environment-based configuration
- Dockerized deployment
- API-first design
  

## System Architecture

### Textual Flow

1. User sends query  
2. Agent layer evaluates intent  
3. If factual → RAG retrieval  
4. If operational → action routing  
5. LLM generates grounded response or structured JSON  
6. Final response returned with citations or action result  



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
  
#### 4. LLM Processing

- LLM receives:
  - Retrieved context (for RAG)
  - Or action schema (for structured output)

#### 5. Response Generation

- Factual answers include:
  - Extracted answer
  - Source page numbers  
- Actions return:
  - JSON with required parameters

#### 6. Action Execution (Mock)

- Action handler simulates enterprise response

---

## Quick Demo


