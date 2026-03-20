def validate_output(output):
    if output is None:
        return {"error": "Empty output"}

    return output