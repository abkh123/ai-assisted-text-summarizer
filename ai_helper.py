#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_helper.py
A Python script interacting with Hugging Face API to generate article summaries.
Author: abkh
Date: May, 2024
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load API Token securely
load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
# API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
# API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6?wait_for_model=true"
API_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum?wait_for_model=true"


headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def generate_summary(article_content):
    import json

    max_length = 1000
    was_truncated = False

    if len(article_content) > max_length:
        was_truncated = True
        print("Input is too long. Truncating...", flush=True)
        article_content = article_content[:max_length] + "..."

    payload = {"inputs": article_content}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        print("RAW HuggingFace response:", response.text, flush=True)  # <--- Add this line

        data = response.json()

        if isinstance(data, list) and "summary_text" in data[0]:
            return {
                "summary": data[0]["summary_text"],
                "truncated": was_truncated
            }
        else:
            print("Unexpected response format:", data, flush=True)
            return {
                "summary": None,
                "truncated": was_truncated
            }

    except Exception as e:
        print("Exception in summary generation:", str(e), flush=True)
        return {
            "summary": None,
            "truncated": False
        }

# When run directly
if __name__ == "__main__":
    test_content = "Artificial intelligence (AI) helps editors quickly summarize and improve article clarity and engagement."
    result = generate_summary(test_content)
    print(json.dumps(result))  # Output JSON string to be parsed by Node.js
