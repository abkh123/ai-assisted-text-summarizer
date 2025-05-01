#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_helper.py
A Python script interacting with Hugging Face API to generate article summaries.
Author: abkh
Date: May, 2024
"""

import os
import requests
from dotenv import load_dotenv

# Load API Token securely
load_dotenv()
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def generate_summary(article_content):
    payload = {"inputs": article_content}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        summary_data = response.json()
        summary_text = summary_data[0]['summary_text'].strip()
        return summary_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Quick test (temporary)
if __name__ == "__main__":
    test_content = "Artificial intelligence (AI) helps editors quickly summarize and improve article clarity and engagement."
    summary_result = generate_summary(test_content)
    print("AI-generated Summary:", summary_result)
