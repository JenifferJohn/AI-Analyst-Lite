import ollama
from config import MODEL


def map_query_columns(query, columns):

    prompt = f"""
User query: {query}

Dataset columns:
{columns}

Map query terms to closest dataset columns.
"""

    res = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return res["message"]["content"]


def generate_code(query, df, history):

    mapping = map_query_columns(query, list(df.columns))

    prompt = f"""
You are a pandas data analyst.

DataFrame name: df

Columns:
{list(df.columns)}

Column grounding:
{mapping}

Conversation history:
{history}

User query:
{query}

Write pandas python code only.

Rules:
- result stored in variable result
- charts must use plotly express px
"""

    res = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return res["message"]["content"]


def fix_code(query, code, error, columns):

    prompt = f"""
The following pandas code failed.

Query:
{query}

Columns:
{columns}

Code:
{code}

Error:
{error}

Return corrected pandas code only.
"""

    res = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return res["message"]["content"]


def summarize(memory):

    if len(memory) == 0:
        return "No analysis results yet."

    text = "\n".join(
        [f"{m['query']} -> {m['preview']}" for m in memory]
    )

    prompt = f"""
Provide a concise business summary of this analysis:

{text}
"""

    res = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return res["message"]["content"]


def is_summary_query(query):

    keywords = [
        "summarize",
        "summary",
        "overall analysis",
        "key insights"
    ]

    return any(k in query.lower() for k in keywords)