import os

project_structure = {
    "casper": {
        "main.py": """
from brain.intent import detect_intent
from brain.router import execute_skill

def main():
    print("🤖 Casper is using local LLM via Ollama. Type something (type 'exit' to quit)\\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        intent = detect_intent(user_input)
        if intent:
            execute_skill(intent, user_input)
        else:
            print("❌ Sorry, I didn’t understand that.")

if __name__ == "__main__":
    main()
""",
        "brain": {
            "__init__.py": "",
            "intent.py": """
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # Or any other local model like "mistral", etc.

def detect_intent(text):
    prompt = f"What is the intent name of this command: '{text}'.\\nRespond ONLY with a single lowercase Python-style function name (e.g., 'hello_world'). Do not explain."
    
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
""",
            "router.py": """
import importlib

def execute_skill(intent, user_input):
    try:
        skill_module = importlib.import_module(f"skills.{intent}")
        if hasattr(skill_module, "run"):
            response = skill_module.run(user_input)
            print("🧠 Casper:", response)
        else:
            print(f"⚠️ Skill '{intent}' has no 'run()' function.")
    except ModuleNotFoundError:
        print(f"❌ Skill '{intent}' not found.")
    except Exception as e:
        print(f"💥 Error running skill '{intent}': {e}")
"""
        },
        "skills": {
            "__init__.py": "",
            "hello_world.py": """
def run(text):
    return "Hello, world! 👋 I am Casper using local LLM."
"""
        }
    }
}


def create_files(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_files(path, content)
        else:
            with open(path, "w") as f:
                f.write(content.strip() + "\\n")


if __name__ == "__main__":
    print("📦 Setting up Casper project with local LLM...")
    create_files(".", project_structure)
    print("✅ Casper created successfully. To run:")
    print("   cd casper && python main.py")