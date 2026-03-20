import requests
import json
from utils.number_formatter import format_number_indian_to_international

OLLAMA_URL = "http://localhost:11434/api/generate"


def format_data_for_llm(data):
    formatted = []

    for row in data:
        new_row = {}
        for key, val in row.items():
            if isinstance(val, (int, float)):
                new_row[key] = format_number_indian_to_international(val)
            else:
                new_row[key] = val
        formatted.append(new_row)

    return formatted


def generate_explanation(data, insights, context, role="non_technical", kpis=None):

    formatted_data = format_data_for_llm(data)

    formatted_kpis = {}

    if kpis:
        formatted_kpis = {
            "current_sales": format_number_indian_to_international(kpis.get("current_sales")),
            "previous_sales": format_number_indian_to_international(kpis.get("previous_sales")),
            "change": format_number_indian_to_international(kpis.get("change")),
            "pct_change": f"{kpis.get('pct_change', 0):.2f}%",
            "top_market": kpis.get("top_market"),
            "top_market_value": format_number_indian_to_international(kpis.get("top_market_value"))
        }

    # Tone control
    if role == "non_technical":
        tone_instruction = """
- Use a casual, conversational tone
- Highlight key takeaway first
"""
    else:
        tone_instruction = """
- Use a professional analytical tone
- Focus on drivers and patterns
"""

    prompt = f"""
You are a business analyst.

STRICT RULES:
- Use ONLY the provided data
- DO NOT calculate anything
- DO NOT hallucinate
- DO NOT change numbers

DATA:
{json.dumps(formatted_data, indent=2)}

KPIs:
{json.dumps(formatted_kpis, indent=2)}

INSIGHTS:
{insights}

CONTEXT:
{context}

TASK:
Explain clearly for business users.

Include:
- Growth or decline (%)
- Previous vs current comparison
- Top performer
- Key takeaway

IMPORTANT:
Use both readable + exact numbers.
Example: "1.2 billion (1,200,000,000)"

TONE:
{tone_instruction}
"""

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code == 200:
            return response.json()["response"].strip()

    except Exception:
        return "Explanation unavailable"

    return "Explanation unavailable"