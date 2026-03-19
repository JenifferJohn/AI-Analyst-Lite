import requests

def ask_llm(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=10
        )
        return res.json()["response"]
    except:
        return "{}"