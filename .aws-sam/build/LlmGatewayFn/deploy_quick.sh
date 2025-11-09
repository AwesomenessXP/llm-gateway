#!/bin/bash

# Quick SAM Deploy Script (non-guided, uses existing samconfig.toml)
# Use this for subsequent deployments after initial guided deploy

set -e

echo "🚀 LLM Gateway Quick Deployment"
echo "==============================="
echo ""

# Check if .env file exists
if [ -f .env ]; then
    echo "📄 Loading API keys from .env..."
    source .env
else
    echo "⚠️  No .env file found"
fi

# Get OpenAI API Key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    read -sp "Enter OpenAI API Key: " OPENAI_API_KEY
    echo ""
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "❌ OpenAI API Key is required"
        exit 1
    fi
fi

# Get Anthropic API Key (optional)
if [ -z "$ANTHROPIC_API_KEY" ]; then
    read -sp "Enter Anthropic API Key (press Enter to skip): " ANTHROPIC_API_KEY
    echo ""
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        ANTHROPIC_API_KEY="placeholder-key"
    fi
fi

echo ""
echo "📦 Building SAM application..."
sam build

echo ""
echo "🚀 Deploying (using samconfig.toml)..."
echo ""

sam deploy \
    --parameter-overrides \
        "OpenAIKey=$OPENAI_API_KEY" \
        "AnthropicKey=$ANTHROPIC_API_KEY"

echo ""
echo "✅ Deployment complete!"

