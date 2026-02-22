import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import json
import random
import time
import requests
import psutil
from dotenv import load_dotenv
import google.generativeai as genai
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
import pywhatkit
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

CONFIG_PATH = "config.json"
try:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
except:
    config = {
        "user_name": "Sir",
        "assistant_name": "V",
        "code_path": "",
        "chrome_path": "",
        "edge_path": ""
    }

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    model = None

chat_history = []

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print(f"{config['assistant_name']}: {text}")
    engine.say(text)
    engine.runAndWait()

def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        volume = devices.EndpointVolume
        if volume:
            level = max(0, min(100, level))
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            return True
    except Exception as e:
        print(f"DEBUG Volume Error: {e}")
        return False
    return False

def get_gemini_response(prompt):
    global chat_history
    if not model:
        return f"I need an API key to think deeply. Please create API key and paste it in .env file"
    
    try:
        context = "\n".join([f"User: {h['u']}\nAI: {h['a']}" for h in chat_history[-5:]])
        full_prompt = f"System: You are {config['assistant_name']}. User Name: {config['user_name']}. Context:\n{context}\nUser: {prompt}\nAI:"
        
        response = model.generate_content(full_prompt)
        ai_response = response.text
        
        chat_history.append({"u": prompt, "a": ai_response})
        return ai_response
    except Exception as e:
        if "429" in str(e):
            return "Energy levels depleted. I have reached my daily limit for deep thinking. Please try again later or upgrade my core."
        return f"Energy levels low. Error: {str(e)}"

def take_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.pause_threshold = 0.8
            r.energy_threshold = 400
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        command = r.recognize_google(audio, language='en-in')
        return command.lower()
    except Exception as e:
        return "None"

def process_query(query):
    if query == "None":
        return None

    if 'wikipedia' in query:
        speak('Searching...')
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia...")
            return results
        except:
            return "No data found on Wikipedia."

    elif 'volume' in query:
        import re
        current_vol = 0
        try:
            devices = AudioUtilities.GetSpeakers()
            volume = devices.EndpointVolume
            if volume:
                current_vol = int(volume.GetMasterVolumeLevelScalar() * 100)
        except: pass

        if 'full' in query:
            level = 100
        elif 'mute' in query or 'zero' in query:
            level = 0
        elif 'half' in query:
            level = 50
        elif 'increase' in query or 'up' in query:
            level = current_vol + 20
        elif 'decrease' in query or 'down' in query:
            level = current_vol - 20
        else:
            nums = re.findall(r'\d+', query)
            level = int(nums[0]) if nums else None
        
        if level is not None:
            if set_volume(level):
                return f"Volume adjusted to {max(0, min(100, level))} percent."
        return "Failed to adjust volume."

    elif 'brightness' in query:
        import re
        current_bri = sbc.get_brightness()[0]
        if 'full' in query:
            level = 100
        elif 'low' in query or 'minimum' in query:
            level = 10
        elif 'half' in query:
            level = 50
        elif 'increase' in query or 'up' in query:
            level = current_bri + 20
        elif 'decrease' in query or 'down' in query:
            level = current_bri - 20
        else:
            nums = re.findall(r'\d+', query)
            level = int(nums[0]) if nums else None
        
        if level is not None:
            level = max(0, min(100, level))
            sbc.set_brightness(level)
            return f"Brightness set to {level} percent."
        return f"Brightness is currenty at {current_bri} percent."

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")
        return "Opening YouTube."

    elif 'open google' in query:
        webbrowser.open("google.com")
        return "Opening Google."

    elif any(word in query for word in ['stop', 'pause', 'mute']) and any(x in query for x in ['music', 'playing', 'youtube', 'video']):
        browsers = ["chrome.exe", "msedge.exe", "brave.exe", "firefox.exe"]
        closed = False
        for browser in browsers:
            if browser in [p.name() for p in psutil.process_iter()]:
                os.system(f"taskkill /F /IM {browser}")
                closed = True
        if closed:
            return "Music stopped."
        return "I couldn't find any music player to stop."

    elif any(word in query for word in ['play', 'song', 'music']):
        song = query.replace("play", "").replace("song", "").replace("music", "").replace("v", "").strip()
        if song:
            speak(f"Playing {song} for you Sir")
            pywhatkit.playonyt(song)
            return f"Playing {song} on YouTube."
        else:
            return "What song should I play, Sir?"

    elif 'close' in query:
        if 'youtube' in query or 'google' in query or 'browser' in query:
            browsers = ["chrome.exe", "msedge.exe", "brave.exe", "firefox.exe"]
            closed = False
            for browser in browsers:
                if browser in [p.name() for p in psutil.process_iter()]:
                    os.system(f"taskkill /F /IM {browser}")
                    closed = True
            return "Closed the browser." if closed else "No browser found to close."
            
    elif 'the time' in query:
        t = datetime.datetime.now().strftime("%H:%M")
        return f"Sir, the time is {t}."

    elif 'cpu' in query:
        return f"CPU utilization is at {psutil.cpu_percent()} percent."

    elif 'battery' in query:
        return f"Power levels at {psutil.sensors_battery().percent} percent."

    elif any(word in query for word in ['exit', 'quit', 'stop']):
        return "SHUTDOWN"

    return get_gemini_response(query)
