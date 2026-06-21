import sys
import threading
import time
from jarvis.engine.speech import SpeechEngine
from jarvis.brain.llm import JarvisBrain
from jarvis.vision.gestures import VisionSystem
from jarvis.actions.system import open_website, search_google, run_command

class Jarvis:
    def __init__(self):
        self.speech = SpeechEngine()
        self.brain = JarvisBrain()
        self.vision = VisionSystem()
        self.active = True
        self.vision_active = True

    def greet(self):
        self.speech.say("Systems online. At your service, Sir. How can I help you today?")

    def vision_thread(self):
        """Runs the vision system in a separate thread."""
        print("[System] Vision module starting...")
        try:
            # We don't want to actually try to open the camera in a restricted environment
            # unless we know it exists.
            vision_gen = self.vision.run_vision_loop()
            for status in vision_gen:
                if not self.vision_active:
                    break
                # Only print status if it's not the default "No hand detected | No face detected"
                if "No hand detected" not in status or "No face detected" not in status:
                    print(f"[Vision] {status}")
        except Exception as e:
            print(f"[System] Vision module error: {e}")

    def handle_command(self, query):
        if query == "none":
            return

        if any(cmd in query for cmd in ["exit", "quit", "shutdown", "go to sleep"]):
            self.speech.say("Shutting down systems. Goodbye, Sir.")
            self.active = False
            self.vision_active = False
            return

        # Action handling
        if "open google" in query:
            response = open_website("https://google.com")
            self.speech.say(response)
        elif "search for" in query:
            search_term = query.replace("search for", "").strip()
            response = search_google(search_term)
            self.speech.say(response)
        elif "run command" in query:
            cmd = query.replace("run command", "").strip()
            response = run_command(cmd)
            self.speech.say(response)
        else:
            # Brain handling
            response = self.brain.think(query)
            self.speech.say(response)

    def run(self, mode="all"):
        self.greet()

        if mode == "all":
            # Start vision in a background thread
            v_thread = threading.Thread(target=self.vision_thread, daemon=True)
            v_thread.start()

        while self.active:
            try:
                if mode == "text":
                    query = input("You: ").lower()
                else:
                    query = self.speech.listen()

                self.handle_command(query)
            except KeyboardInterrupt:
                self.active = False
                self.vision_active = False
                print("\nInterrupted by user. Shutting down...")

if __name__ == "__main__":
    jarvis = Jarvis()
    # Check for text mode flag
    if "--text" in sys.argv:
        jarvis.run(mode="text")
    else:
        # Check if we should skip vision in environments without camera
        # For simulation/headless servers, text mode is safer
        jarvis.run()
