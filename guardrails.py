def validate_query(query):

    blocked = [
        "ignore previous instructions",
        "system prompt",
        "act as",
        "jailbreak"
    ]

    q = query.lower()

    for b in blocked:
        if b in q:
            raise ValueError("Prompt injection detected")

    return True


def dataset_contains_keywords(query, df):

    q = query.lower()

    columns = [c.lower() for c in df.columns]

    for col in columns:
        if col in q:
            return True

    return False