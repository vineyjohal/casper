import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # Or any other local model like "mistral", etc.

def detect_intent(text):
    prompt = f"What is the intent name of this command: '{text}'.\nRespond ONLY with a single lowercase Python-style function name (e.g., 'hello_world'). Do not explain."
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        result = response.json()["response"].strip().split()[0]  # only first word
        return result if result.isidentifier() else None
    except Exception as e:
        print("❌ Intent detection error:", e)
        return None