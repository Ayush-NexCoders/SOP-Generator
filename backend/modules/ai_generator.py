"""
AI Generator Module
Uses Groq API to generate business analysis and SOP content.
"""
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    return Groq(api_key=api_key)

def generate_context(analysis_prompt: str) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a business process analyst. Return only the structured "
                    "analysis format as instructed. No extra text."
                ),
            },
            {"role": "user", "content": analysis_prompt},
        ],
        temperature=0.3,
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()

def generate_sop(sop_prompt: str) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior enterprise SOP writer. "
                    "Return only the SOP in the exact plain-text format specified. "
                    "No markdown, no tables, no extra commentary."
                ),
            },
            {"role": "user", "content": sop_prompt},
        ],
        temperature=0.4,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()
