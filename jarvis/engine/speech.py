import pyttsx3
import speech_recognition as sr
import os

class SpeechEngine:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            # Try to find a voice that sounds somewhat like JARVIS
            for voice in voices:
                if "british" in voice.name.lower() or "english" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            self.engine.setProperty('rate', 175)
            self.enabled = True
        except Exception as e:
            print(f"Speech engine initialization failed: {e}")
            self.enabled = False

    def say(self, text):
        print(f"JARVIS: {text}")
        if self.enabled:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass

    def listen(self):
        if not self.enabled:
            return input("User (Text Mode): ").lower()

        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source, timeout=5, phrase_time_limit=5)

            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except Exception as e:
            print(f"Listening error: {e}")
            return "none"
