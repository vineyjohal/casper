from brain.intent import detect_intent
from brain.router import execute_skill

def main():
    print("🤖 Casper is using local LLM via Ollama. Type something (type 'exit' to quit)\n")
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