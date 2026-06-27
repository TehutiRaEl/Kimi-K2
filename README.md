# Kimi-K2 — Mind Colony (Language Model Gateway)

[![Colony](https://img.shields.io/badge/colony-colony-purple)](#)
[![Archetype](https://img.shields.io/badge/archetype-mind-blueviolet)](#)
[![Layer](https://img.shields.io/badge/layer-3%20MIND%20(AZR)-purple)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![Hive](https://img.shields.io/badge/hive-sovereign--hive-gold)](#)

> Kimi K2 language model interface and reasoning gateway for the Sovereign Hive — 128K context, agentic intelligence.

## Role in the Sovereign Hive

| Field | Value |
|-------|-------|
| colony_id | `kimi-k2` |
| role | colony |
| archetype | mind |
| layer | 3 (MIND — The AZR) |
| entity | MIND (The AZR) |
| guilds | reasoning, language, inference |
| queen | THEHIVE :8080 |
| port | 8002 |

## What This Does

Kimi-K2 is the Mind colony — a FastAPI service that wraps the Kimi K2 language model as a hive-native reasoning gateway. It exposes:

- **OpenAI-compatible `/v1/chat/completions`** — drop-in replacement for any OpenAI client
- **128K context window** — Kimi K2 Instruct via Moonshot AI API
- **Automatic fallback** — if no `KIMI_API_KEY` is set, routes to THEHIVE's local LLM gateway
- **Colony Standard Layer** — full `/colony/*` endpoints for hive integration
- **Agent identity** — registers as `kimi-k2-primary` in the hive agent roster

## Quick Start

```bash
git clone https://github.com/TehutiRaEl/Kimi-K2
cd Kimi-K2
cp .env.example .env
# Add KIMI_API_KEY from https://platform.moonshot.cn/
pip install -r requirements.txt
python main.py
```

Or with Docker:
```bash
docker-compose up -d
```

The service starts on `http://localhost:8002`.

## Colony Standard Layer

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/colony/health` | Live health + uptime |
| GET | `/colony/info` | Colony identity, model, context length |
| GET | `/colony/manifest` | Endpoints + capabilities |
| POST | `/colony/events` | Accept hive dispatch events |
| GET | `/colony/agents` | Kimi-K2 primary agent |

## LLM Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/chat/completions` | OpenAI-compatible chat completion |

### Request Format

```json
{
  "model": "kimi-k2",
  "messages": [
    {"role": "user", "content": "Explain the Sovereign Hive constitution."}
  ],
  "max_tokens": 2048,
  "stream": false
}
```

## Architecture

```
Kimi-K2 (mind / layer 3) :8002
├── main.py           # FastAPI app with all endpoints
├── requirements.txt  # fastapi, uvicorn, httpx, pydantic
├── colony.json       # Colony identity manifest
├── soul.md           # F-001–F-006 constitution (synced from Queen)
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── .github/workflows/
    └── constitution-receive.yml  # Auto-sync soul.md from Queen
```

## LLM Routing

```
POST /v1/chat/completions
    │
    ├── KIMI_API_KEY set?
    │       YES → Moonshot AI API (kimi-k2-instruct, 128K context)
    │       NO  → QUEEN_URL/v11/llm/chat (THEHIVE local Ollama fallback)
    │
    └── Response (OpenAI format)
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8002` | Listen port |
| `QUEEN_URL` | `http://localhost:8080` | THEHIVE Queen URL (fallback LLM) |
| `KIMI_API_KEY` | *(optional)* | Moonshot AI API key |
| `KIMI_API_URL` | `https://api.moonshot.cn/v1` | Kimi API base URL |

Get a Kimi API key from [platform.moonshot.cn](https://platform.moonshot.cn/).

## Constitution Sync

Receives `soul.md` updates automatically from the Queen via `.github/workflows/constitution-receive.yml`.

## About the Kimi K2 Model

Kimi K2 is a Mixture-of-Experts language model from Moonshot AI with:
- **1 trillion total parameters** (32B activated per token)
- **128K context window**
- Optimized for agentic tasks, tool use, and complex reasoning
- Open weights available on [Hugging Face](https://huggingface.co/moonshotai)

For self-hosted inference, download the model weights and point `KIMI_API_URL` to your local inference server.

## Contributing

PRs that expand reasoning capabilities, improve the fallback routing, or add streaming support are welcome.
