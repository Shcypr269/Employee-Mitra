from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from config import AgentConfig
from agent import AgenticRAGAssistant


app = FastAPI(title="Agentic RAG API")

# ✅ CORS for Flutter / Web / Mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = AgentConfig.from_env()
assistant = AgenticRAGAssistant(config)

if not assistant.initialize():
    raise RuntimeError("Failed to initialize assistant")


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    answer: str
    intent: str
    confidence: float
    response_type: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = assistant.process_query(req.query)

    if result.get("error"):
        return {
            "answer": result["error"],
            "intent": "error",
            "confidence": 0.0,
            "response_type": "error",
        }

    return {
        "answer": result.get("answer") or result.get("explanation"),
        "intent": result["intent"]["intent_type"],
        "confidence": result["retrieval"]["confidence"],
        "response_type": result["response_type"],
    }
