#!/bin/bash

# Load API key from .env file
source .env

echo "Testing Google Gemini API key..."
echo "API Key: ${GOOGLE_API_KEY:0:20}..." # Show only first 20 chars for security

# Test the API key
response=$(curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=${GOOGLE_API_KEY}")

# Check if the response contains an error
if echo "$response" | grep -q '"error"'; then
    echo "❌ API Key is INVALID"
    echo "Error details:"
    echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    exit 1
else
    echo "✅ API Key is VALID"
    echo "Available models:"
    echo "$response" | python3 -m json.tool 2>/dev/null | grep '"name"' | head -5
    exit 0
fi
