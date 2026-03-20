import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_explanation(data, insights, context, role="non_technical"):
    """
    Generates human-friendly narrative using Ollama (Mistral).
    STRICT: No calculations, no hallucination.
    """

    tone_instruction = ""

    if role == "non_technical":
        tone_instruction = """
- Use a casual, conversational tone
- Explain like you're talking to a business manager
- Highlight key takeaway first
- Keep it short and clear
"""
    else:
        tone_instruction = """
- Use a professional analytical tone
- Mention key drivers and patterns
- Be concise but insightful
"""

    prompt = f"""
You are a business analyst.

STRICT RULES:
- Use ONLY the provided data
- DO NOT calculate anything
- DO NOT assume missing values
- DO NOT hallucinate
- DO NOT change numbers

TONE:
{tone_instruction}

DATA:
{json.dumps(data, indent=2)}

INSIGHTS:
{insights}

CONTEXT:
{context}

TASK:
Write a clear explanation of the results.
Focus on:
- What is happening
- Any standout patterns
- Key takeaway

Keep it short (3–5 sentences max).
"""

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2  # slight natural tone, still controlled
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code == 200:
            return response.json()["response"].strip()

    except Exception:
        return "Explanation unavailable"

    return "Explanation unavailable"