#!/usr/bin/env python3
"""Test script for LLM Gateway endpoint"""

import requests
import json
import sys

ENDPOINT = "https://s2463c0bjg.execute-api.us-east-1.amazonaws.com/v1/chat/completions"

def test_endpoint():
    """Test the LLM Gateway endpoint"""
    
    # Test payload
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": "Say hello in one word"}
        ]
    }
    
    print(f"Testing endpoint: {ENDPOINT}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(
            ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print("-" * 50)
        
        try:
            response_json = response.json()
            print(f"Response Body:\n{json.dumps(response_json, indent=2)}")
            
            # Check for errors
            if "detail" in response_json:
                print("\n❌ Error detected:", response_json["detail"])
                if "401" in str(response_json.get("detail", "")):
                    print("\n⚠️  401 Unauthorized - Check if OPENAI_API_KEY is set in Lambda environment variables")
            elif "choices" in response_json:
                print("\n✅ Success! Response received:")
                if response_json.get("choices"):
                    print(f"Message: {response_json['choices'][0]['message']['content']}")
        except json.JSONDecodeError:
            print(f"Response Text: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_endpoint()

