import requests

# LM Studio local API endpoint
API_URL = "http://10.0.0.48:1234/v1/chat/completions"
MODEL = "llama-3.2-3b-instruct"

def chat_with_bot():
    print("🤖 LM Studio Chatbot (type 'exit' to quit)\n")

    messages = [
        {"role": "system", "content": "You are a helpful and friendly assistant."}
    ]

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        messages.append({"role": "user", "content": user_input})

        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0.7
            }
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            print("Bot:", reply)
            messages.append({"role": "assistant", "content": reply})
        else:
            print("❌ Error:", response.text)

if __name__ == "__main__":
    chat_with_bot()