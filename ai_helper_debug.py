#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_helper_debug.py
Debug version to diagnose Hugging Face API connection issues
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables and check token
print("Checking environment setup...")
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
print(f"Token loaded: {HUGGINGFACE_API_TOKEN is not None}")
print(f"Token length: {len(HUGGINGFACE_API_TOKEN) if HUGGINGFACE_API_TOKEN else 0}")
print(f"First few chars (if any): {HUGGINGFACE_API_TOKEN[:5] + '...' if HUGGINGFACE_API_TOKEN and len(HUGGINGFACE_API_TOKEN) > 5 else HUGGINGFACE_API_TOKEN}")

# Try a different approach - setting token directly for testing
# Comment this out once you've verified the .env loading works
TEST_TOKEN = "hf_wwwwwwwwwwwwwwwwwwwwwwwwww"  # Replace with your actual token for testing
print(f"Using test token: {TEST_TOKEN[:5] + '...' if len(TEST_TOKEN) > 5 else TEST_TOKEN}")

# Try both API URL formats
API_URL_1 = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_URL_2 = "https://api-inference.huggingface.co/pipeline/summarization/facebook/bart-large-cnn"

def test_api_connection(url, token):
    """Test basic API connectivity"""
    print(f"\nTesting connection to: {url}")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Just do a GET request to check if the endpoint exists
        response = requests.get(url, headers=headers)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:100]}...")
        return response.status_code
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def generate_summary(article_content, url, token):
    """Attempt to generate a summary using the specified URL and token"""
    print(f"\nAttempting summary with: {url}")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": article_content}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                summary_data = response.json()
                print(f"Response JSON type: {type(summary_data)}")
                print(f"Response JSON content: {summary_data}")
                
                if isinstance(summary_data, list) and len(summary_data) > 0:
                    summary_text = summary_data[0].get('summary_text', '').strip()
                    return summary_text
                else:
                    print(f"Unexpected response format")
                    return None
            except Exception as e:
                print(f"Error parsing response: {e}")
                return None
        else:
            print(f"Error response code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

if __name__ == "__main__":
    # Test if we can even connect to the API
    print("\n--- Testing with env file token ---")
    test_api_connection(API_URL_1, HUGGINGFACE_API_TOKEN)
    
    print("\n--- Testing with direct token ---")
    test_api_connection(API_URL_1, TEST_TOKEN)
    
    # Try both URLs with the direct token
    print("\n--- Testing alternate API URL ---")
    test_api_connection(API_URL_2, TEST_TOKEN)
    
    # Test the actual summarization
    test_content = "Artificial intelligence (AI) helps editors quickly summarize and improve article clarity and engagement."
    
    print("\n--- Testing summarization ---")
    summary_result = generate_summary(test_content, API_URL_1, TEST_TOKEN)
    print("\nFinal summary result:", summary_result)