#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_helper.py
A Python script for interacting with OpenAI's GPT API to generate article summaries.
Author: abkh
Date: May 2024
"""

from  openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key securely
load_dotenv()
client = OpenAI()

def generate_summary(article_content):
    prompt = f"Summarize the following article clearly and concisely:\n\n{article_content}\n\nSummary:"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "developer", "content": "You are an assistant that summarizes articles."},
                {"role": "user", "content": prompt}
            ],

        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Quick test (temporary)
if __name__ == "__main__":
    test_content = "Artificial intelligence (AI) helps editors quickly summarize and improve article clarity and engagement."
    summary_result = generate_summary(test_content)
    print("AI-generated Summary:", summary_result)
