"""
Kimi-K2 Mind Colony — Sovereign Hive
Language model inference gateway for the Mind Trinity node.
Routes to Kimi API (Moonshot AI) if key present, falls back to THEHIVE LLM gateway.
Exposes Colony Standard Layer + OpenAI-compatible /v1/chat/completions.
"""

import hashlib
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Kimi-K2 Mind Colony", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_start = datetime.now()
QUEEN_URL = os.getenv("QUEEN_URL", "http://localhost:8080")
KIMI_API_KEY = os.getenv("KIMI_API_KEY", "")
KIMI_API_URL = os.getenv("KIMI_API_URL", "https://api.moonshot.cn/v1")
PORT = int(os.getenv("PORT", "8002"))


def _soul_hash() -> str:
    try:
        soul_path = os.path.join(os.path.dirname(__file__), "soul.md")
        return hashlib.sha256(open(soul_path, "rb").read()).hexdigest()[:16]
    except Exception:
        return "none"


# ─── Colony Standard Layer ────────────────────────────────────────────────────

@app.get("/colony/health")
def colony_health():
    uptime = int((_start and (datetime.now() - _start).total_seconds()) or 0)
    return {"status": "healthy", "colony_id": "kimi-k2", "timestamp": datetime.now().isoformat(),
            "uptime_seconds": uptime}


@app.get("/colony/info")
def colony_info():
    return {
        "colony_id": "kimi-k2", "colony_name": "Kimi-K2", "role": "colony",
        "archetype": "mind", "layer": 3, "entity": "MIND (The AZR)",
        "guilds": ["reasoning", "language", "inference"],
        "hive": "sovereign-hive", "queen": "https://github.com/TehutiRaEl/-sovereign-hive-meta",
        "version": "1.0.0", "soul_md_hash": _soul_hash(), "port": PORT,
        "model": "kimi-k2-instruct", "context_length": 131072,
    }


@app.get("/colony/manifest")
def colony_manifest():
    return {
        "colony_id": "kimi-k2",
        "endpoints": ["/colony/health", "/colony/info", "/colony/manifest",
                      "/colony/events", "/colony/agents", "/v1/chat/completions"],
        "capabilities": ["reasoning", "language_model", "inference", "128k_context",
                         "tool_use", "multimodal"],
        "version": "1.0.0",
    }


@app.post("/colony/events")
def colony_events(event: Dict[str, Any]):
    return {"event_id": str(uuid.uuid4()), "status": "received", "colony_id": "kimi-k2"}


@app.get("/colony/agents")
def colony_agents():
    return [{"agent_id": "kimi-k2-primary", "name": "Kimi", "status": "active",
             "role": "language_model", "model": "kimi-k2-instruct"}]


# ─── OpenAI-compatible chat endpoint ─────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "kimi-k2"
    messages: List[ChatMessage]
    max_tokens: int = 2048
    temperature: float = 0.7
    stream: bool = False


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest):
    """Route to Kimi API if key configured, else proxy through THEHIVE LLM gateway."""
    msgs = [{"role": m.role, "content": m.content} for m in req.messages]

    if KIMI_API_KEY:
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                r = await client.post(
                    f"{KIMI_API_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {KIMI_API_KEY}",
                             "Content-Type": "application/json"},
                    json={"model": "kimi-k2-instruct", "messages": msgs,
                          "max_tokens": req.max_tokens, "temperature": req.temperature},
                )
                r.raise_for_status()
                return r.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e))
    else:
        # Fall back to THEHIVE LLM gateway
        prompt = msgs[-1]["content"] if msgs else ""
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                r = await client.post(
                    f"{QUEEN_URL}/v11/chat/completions",
                    json={"model": "auto", "messages": msgs,
                          "max_tokens": req.max_tokens},
                )
                r.raise_for_status()
                return r.json()
            except Exception as e:
                raise HTTPException(status_code=503, detail=f"LLM gateway unavailable: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
