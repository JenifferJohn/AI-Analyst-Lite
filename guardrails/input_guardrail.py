def validate_user_query(query):
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    blocked = ["ignore previous", "system prompt", "act as"]

    q = query.lower()

    for b in blocked:
        if b in q:
            raise ValueError("Unsafe query detected")

    return query