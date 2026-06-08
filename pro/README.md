# 🤖 AI Agent Pro Kit — Pro Deployment Guide

## Prerequisites

- Docker & Docker Compose
- Git
- 2GB+ RAM, 10GB+ disk

## One-Click Deploy

```bash
cd pro
docker-compose up -d
```

This starts:
- **FreeLLMAPI** on port `3100` — 98 models behind one OpenAI-compatible API
- **Agent Reach** CLI ready — autonomous web research

## Verify

```bash
# Check FreeLLMAPI
curl http://localhost:3100/v1/models

# Check Agent Reach
agent-reach --help
```

## Configure

Set your FreeLLMAPI as the default AI backend:

```bash
# OpenAI-compatible: any app that supports custom endpoints
export OPENAI_BASE_URL=http://localhost:3100/v1
export OPENAI_API_KEY=sk-your-key
```

## Hermes Integration

Add to your Hermes config:

```yaml
providers:
  freellmapi:
    base_url: http://localhost:3100/v1
    api_key: sk-your-key
    models:
      - gpt-4o-mini-free
      - claude-3-haiku-free
      - deepseek-chat-free
      - gemini-2.0-flash-free
```
