#!/bin/bash
set -e

# AI Agent Pro Kit — Pro Setup Script
# One-command deployment

echo "🤖 AI Agent Pro Kit — Setup"
echo "=========================="

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker required. Install: https://docker.com"; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose required"; exit 1; }

# Parse args
FREEL_KEY="${1:-sk-pro-default}"
ADMIN_EMAIL="${2:-admin@example.com}"

echo ""
echo "📦 Deploying FreeLLMAPI (98 models)..."
echo "   Key: $FREEL_KEY"
echo "   Admin: $ADMIN_EMAIL"
echo ""

# Create data dirs
mkdir -p pro/data pro/config pro/config/agent_reach

# Launch
export FREEL_API_KEY="$FREEL_KEY"
export ADMIN_EMAIL="$ADMIN_EMAIL"
cd pro && docker-compose up -d

echo ""
echo "✅ Done! FreeLLMAPI running on http://localhost:3100"
echo ""
echo "📋 Quick test:"
echo "   curl http://localhost:3100/v1/models | jq '.data | length'"
echo ""
echo "🔌 Set as your AI backend:"
echo "   export OPENAI_BASE_URL=http://localhost:3100/v1"
echo "   export OPENAI_API_KEY=$FREEL_KEY"
