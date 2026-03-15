import ollama

def generate_analysis_code(query, df):
    columns = list(df.columns)
    schema = df.dtypes.to_string()
    prompt = f"""
You are a Python data analyst.
Dataset columns:
{columns}

Schema:
{schema}

User question:
{query}

Write ONLY pandas Python code using dataframe 'df'.

Rules:
- Use only existing columns
- Return dataframe or series
- Use groupby for trends
- Use corr() for correlations

Return only Python code.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0}
    )

    return response["message"]["content"].strip()