#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_helper_openrouter.py
Reliable AI summarizer using OpenRouter API (e.g., GPT-3.5).
Author: abkh
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
# API_KEY = os.getenv("TOGETHER_API_KEY")

if not API_KEY:
    print("OpenRouter API key not found in .env file.")
    exit(1)

# API_URL = "https://openrouter.ai/api/v1/chat"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = "openai/gpt-3.5-turbo"
# MODEL = "mistralai/mistral-7b-instruct"


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:3000",  # Required by OpenRouter
    "X-Title": "AI Content Summarizer"
}

def generate_summary(article_content):
    max_length = 3000
    was_truncated = False

    if len(article_content) > max_length:
        was_truncated = True
        article_content = article_content[:max_length] + "..."

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes articles or technical content clearly and concisely."},
            {"role": "user", "content": f"Summarize this:\n\n{article_content}"}
        ]
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE TEXT:", repr(response.text))  # <- use repr to show empty string

        if response.status_code != 200:
            return { "summary": None, "truncated": was_truncated }

        data = response.json()
        summary_text = data["choices"][0]["message"]["content"].strip()

        return {
            "summary": summary_text,
            "truncated": was_truncated
        }


    except Exception as e:
        print("Exception in OpenRouter API:", str(e), flush=True)
        return {
            "summary": None,
            "truncated": False
        }

# Local test
if __name__ == "__main__":
    test_input = "Machine learning improves healthcare by predicting disease and recommending treatments."
    result = generate_summary(test_input)
    print(json.dumps(result, indent=2))
