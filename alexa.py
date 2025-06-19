# Enhanced Alexa Assistant with:
# 1. Reminders & Scheduling
# 2. Smart Home Automation (simulated)
# 3. Multilingual Support

import speech_recognition as sr
import datetime
import webbrowser
import os
import requests
import pygame
import time
from gtts import gTTS
from bs4 import BeautifulSoup
import json
import threading
from plyer import notification
from googletrans import Translator

# Initialize pygame mixer
pygame.mixer.init()

# Language setting
LANG = 'en'

# --- SPEAK FUNCTION ---
def speak(text, lang=LANG):
    print("Speaking:", text)
    tts = gTTS(text=text, lang=lang)
    tts.save("voice.mp3")
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.unload()
    os.remove("voice.mp3")

# --- TRANSLATION SUPPORT ---
translator = Translator()

def translate_text(text, to_lang='en'):
    try:
        result = translator.translate(text, dest=to_lang)
        return result.text
    except Exception as e:
        print("Translation error:", e)
        return "Translation failed."

# --- WISHING FUNCTION ---
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!", LANG)
    elif 12 <= hour < 18:
        speak("Good afternoon!", LANG)
    else:
        speak("Good evening!", LANG)
    speak("I am Alexa. How can I help you today?", LANG)

# --- VOICE INPUT FUNCTION ---
def take_command():
    r = sr.Recognizer()
    with sr.Microphone(device_index=3) as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.7)
        r.pause_threshold = 1.2
        audio = r.listen(source, timeout=10, phrase_time_limit=8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)
        return query.lower()
    except sr.WaitTimeoutError:
        print("Listening timed out")
        return "none"
    except sr.UnknownValueError:
        print("Sorry, could not understand.")
        speak("Say that again please.", LANG)
        return "none"
    except sr.RequestError:
        print("Network error.")
        speak("Network issue, please check your connection.", LANG)
        return "none"

# --- TEMPERATURE FETCH FUNCTION ---
def get_temperature(query):
    api_key = "734c988c8a091754f544065ef35a413c"  # Replace with your actual API key
    city = "ahmedabad"
    if "in" in query:
        city = query.split("in")[-1].strip()

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        )
        r = requests.get(url)
        data = r.json()
        if data.get("cod") != 200:
            speak("City not found. Please try again.", LANG)
            return

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp}°C with {desc}.", LANG)
    except Exception as e:
        print("Weather fetch error:", e)
        speak("Sorry, I couldn't fetch the weather.", LANG)

# --- REMINDER SETTER ---
def set_reminder(task, delay):
    def remind():
        time.sleep(delay)
        notification.notify(title="Reminder", message=task, timeout=10)
        speak(f"Reminder: {task}", LANG)
    threading.Thread(target=remind).start()

# --- HOME AUTOMATION (SIMULATED) ---
def control_device(device, state):
    speak(f"Turning {state} the {device}.", LANG)

# --- MAIN FUNCTION ---
if __name__ == "__main__":
    wish_me()

    while True:
        query = take_command()

        if 'open youtube' in query:
            speak("Opening YouTube.", LANG)
            webbrowser.open("https://www.youtube.com")

        elif 'hello alexa' in query:
            speak("Hello sir, how are you", LANG)

        elif 'i am fine' in query:
            speak("That's Great, sir", LANG)

        elif 'how are you' in query:
            speak("I am fine sir, thanks for asking", LANG)

        elif 'you are so good' in query:
            speak("Thank you sir, I'm trying to be a great assistant for you.", LANG)

        elif 'open google' in query:
            speak("Opening Google.", LANG)
            webbrowser.open("https://www.google.com")

        elif 'temperature' in query:
            get_temperature(query)

        elif 'play music' in query:
            speak("Playing your music.", LANG)
            webbrowser.open("https://youtu.be/QQmA1LM1LiM?si=pzAXT0f8Rg26FGXv")

        elif 'time' in query:
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {time_str}", LANG)

        elif 'remind me to' in query:
            try:
                parts = query.split('remind me to')[1].strip().split(' in ')
                task = parts[0].strip()
                mins = int(parts[1].replace('minutes', '').strip())
                speak(f"Reminder set for {task} in {mins} minutes", LANG)
                set_reminder(task, mins * 60)
            except:
                speak("Sorry, I could not set the reminder.", LANG)

        elif 'turn on light' in query:
            control_device("light", "on")

        elif 'turn off fan' in query:
            control_device("fan", "off")

        elif 'translate' in query:
            speak("What should I translate?", LANG)
            phrase = take_command()

            speak("To which language? Like 'Hindi', 'Gujarati', or 'French'", LANG)
            lang_input = take_command().lower()

            lang_map = {
                'hindi': 'hi',
                'gujarati': 'gu',
                'french': 'fr',
                'german': 'de',
                'english': 'en'
            }

            to_lang = lang_map.get(lang_input, 'en')
            translated_text = translate_text(phrase, to_lang)
            speak(f"Translated to {lang_input}: {translated_text}", to_lang)

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a great day.", LANG)
            break