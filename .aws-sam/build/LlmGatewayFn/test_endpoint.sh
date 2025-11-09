#!/bin/bash

# Test script for LLM Gateway endpoint
ENDPOINT="https://s2463c0bjg.execute-api.us-east-1.amazonaws.com/v1/chat/completions"

echo "Testing endpoint: $ENDPOINT"
echo ""

# Test 1: Simple hello message
echo "Test 1: Simple hello message"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Say hello in one word"}
    ]
  }' | jq '.'

echo ""
echo "---"
echo ""

# Test 2: More complex conversation
echo "Test 2: Complex conversation"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is 2+2?"}
    ]
  }' | jq '.'

echo ""
echo "---"
echo ""

# Test 3: Check response structure
echo "Test 3: Full response"
curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "Hi"}
    ]
  }' | jq '.'

