# main.py

import json
import os
import requests
import pyttsx3
import speech_recognition as sr
from config import API_URL, MODEL_NAME, TEMPERATURE, MEMORY_FILE

# 🔊 Text-to-speech setup
engine = pyttsx3.init()
engine.setProperty("rate", 170)

# 🎙️ Speech recognizer
recognizer = sr.Recognizer()

# 🧠 Load memory
def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                data = f.read().strip()
                if data:
                    return json.loads(data)
        except json.JSONDecodeError:
            print("⚠️ Memory file is corrupted. Resetting...")
    return [{"role": "system", "content": "You are Casper, a smart and friendly AI assistant."}]

# 🧠 Save memory
def save_memory(messages):
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

# 🎤 Get voice input
def get_voice_input():
    try:
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
    except sr.UnknownValueError:
        print("❌ Sorry, I didn't catch that.")
    except sr.RequestError:
        print("❌ Could not reach the speech recognition service.")
    except Exception as e:
        print("⚠️ Voice input error:", e)

    # fallback to manual typing
    return input("📝 Type instead: ")

# 🤖 Get response from LM Studio
def get_response(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": TEMPERATURE
    }
    try:
        response = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ API Error:", e)
        return "Sorry, I had a problem reaching my brain."

# 🔁 Chat loop
def start_casper():
    print("🤖 Casper with Voice + Memory")
    print("Say something or type (or type 'exit' to quit)\n")

    messages = load_memory()

    while True:
        choice = input("🎧 (V)oice or (T)ext? ").strip().lower()

        if choice == "v":
            user_input = get_voice_input()
        else:
            user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Bye!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        reply = get_response(messages)
        print("Casper:", reply)
        engine.say(reply)
        engine.runAndWait()

        messages.append({"role": "assistant", "content": reply})
        save_memory(messages)

if __name__ == "__main__":
    start_casper()