import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_columns(columns):
    return {c:model.encode(c) for c in columns}

def embed_query(query):
    return model.encode(query)

def map_column(query, embeddings):

    q = embed_query(query)

    best=None
    score=-1

    for col,vec in embeddings.items():

        s = np.dot(q,vec)

        if s > score:
            score=s
            best=col

    return best


def classify_intent(query):

    prompt=f"""
Classify analytics intent.

Query:
{query}

Possible intents:
summary
trend
groupby
share
correlation
drivers
anomaly
insight
report
unknown

Return JSON:
{{"intent":"","confidence":0.0}}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role":"user","content":prompt}]
    )

    try:
        result=eval(response["message"]["content"])
        return result["intent"], result["confidence"]
    except:
        return "unknown",0.0


def generate_insight(query,result,persona):

    prompt=f"""
User query:
{query}

Result table:
{result}

Rules:
Only use numbers present in table.
Do not invent variables.

Explain insights clearly.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]