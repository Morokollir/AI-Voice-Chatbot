import openai
import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize speech recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def listen_for_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I did not catch that."
    except sr.RequestError as e:
        return f"Error: {e}"

def speak_text(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print("Say something (or 'exit' to quit):")
    while True:
        user_input = listen_for_speech()
        print("You:", user_input)
        if user_input.lower() == "exit":
            break
        reply = chat_with_gpt(user_input)
        print("AI:", reply)
        speak_text(reply)
