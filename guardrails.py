def validate_query(query):

    blocked = [
        "ignore previous instructions",
        "system prompt",
        "jailbreak"
    ]

    q = query.lower()

    for word in blocked:
        if word in q:
            raise ValueError("Prompt injection detected")

    return True