import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"


def ask_llm(prompt, model=MODEL):
    """Ollama se baat karo aur uska jawab (text) wapas do."""
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["message"]["content"].strip()
    except Exception as e:
        return f"[LLM error: {e}. Kya Ollama chal raha hai? Terminal me 'ollama list' chalao.]"
