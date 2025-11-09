#!/bin/bash

# Find the Lambda function name
echo "Finding Lambda function..."
FUNCTION_NAME=$(aws lambda list-functions --query 'Functions[?contains(FunctionName, `LlmGateway`)].FunctionName' --output text)

if [ -z "$FUNCTION_NAME" ]; then
    echo "❌ Could not find LlmGateway function"
    echo "Available functions:"
    aws lambda list-functions --query 'Functions[].FunctionName' --output table
    exit 1
fi

echo "Found function: $FUNCTION_NAME"
echo ""
echo "Current environment variables:"
aws lambda get-function-configuration \
  --function-name "$FUNCTION_NAME" \
  --query 'Environment.Variables' \
  --output json | jq '.'

