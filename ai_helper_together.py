#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_helper_together.py
Summarization helper using Together.ai and Mixtral-8x7B.
Author: abkh
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

API_URL = "https://api.together.xyz/v1/chat/completions"
# MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
# MODEL = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_summary(article_content):
    max_length = 5000
    was_truncated = False

    if len(article_content) > max_length:
        was_truncated = True
        article_content = article_content[:max_length] + "..."

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an assistant that summarizes technical and general text clearly."},
            {"role": "user", "content": f"Summarize this:\n\n{article_content}"}
        ],
        "max_tokens": 5000,
        "temperature": 0.3
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code != 200:
            print("Together.ai HTTP", response.status_code, "→", response.text, flush=True)
            return { "summary": None, "truncated": was_truncated }

        data = response.json()
        summary_text = data["choices"][0]["message"]["content"].strip()

        return {
            "summary": summary_text,
            "truncated": was_truncated
        }

    except Exception as e:
        print("Together.ai Exception:", str(e), flush=True)
        return {
            "summary": None,
            "truncated": False
        }

# Local test
if __name__ == "__main__":
    text = "ROS2 is an advanced robotics middleware framework used for modular and scalable robot software development."
    result = generate_summary(text)
    print(json.dumps(result, indent=2))
