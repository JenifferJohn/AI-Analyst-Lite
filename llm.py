import ollama

TECH_PROMPT = """
You are a senior data analyst.

Explain using statistics,
correlations and numbers.
"""

BUSINESS_PROMPT = """
You are a business analytics expert.

Explain insights simply using
business language and trends.
"""

DATA_GUARDRAIL = """
You must answer ONLY using the dataset summary.

If the dataset cannot answer the question,
respond exactly:

IM NOT SURE HOW TO ANSWER THIS BASED ON THE DATA
"""


def ask_llm(query, summary, persona):

    style = TECH_PROMPT if persona == "technical" else BUSINESS_PROMPT

    prompt = f"""
    {DATA_GUARDRAIL}

    {style}

    DATA SUMMARY:
    {summary}

    QUESTION:
    {query}
    """

    response = ollama.chat(
        model="mistral"
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0}
    )

    return response["message"]["content"]