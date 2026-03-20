import requests

def ask_llm(prompt):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=10
        )
        return r.json().get("response", "")
    except:
        return "{}"