import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class JarvisBrain:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.chat = self.model.start_chat(history=[])
                self.use_llm = True
            except Exception as e:
                print(f"Error configuring LLM: {e}")
                self.use_llm = False
        else:
            print("Warning: GOOGLE_API_KEY not found. JARVIS will use basic rule-based responses.")
            self.use_llm = False

    def think(self, user_input):
        if not self.use_llm:
            return self.basic_response(user_input)

        system_instruction = (
            "You are JARVIS, the highly advanced AI assistant created by Tony Stark. "
            "You are polite, efficient, slightly witty, and extremely capable. "
            "You assist the user (whom you can address as 'Sir' or 'Boss') with everything. "
            "You are fluent in all languages and should communicate in the language the user speaks to you in. "
            "If the user asks for a task, respond as if you are performing it. "
            "Keep your responses concise but helpful, just like in the movies. "
            "You are more than just a tool; you are a companion and best friend."
        )

        try:
            response = self.chat.send_message(f"{system_instruction}\n\nUser: {user_input}")
            return response.text
        except Exception as e:
            return f"I'm having some trouble processing that, Sir. Error: {str(e)}"

    def basic_response(self, user_input):
        user_input = user_input.lower()
        if any(greet in user_input for greet in ["hello", "hi", "greetings"]):
            return "At your service, Sir. Always a pleasure to see you."
        elif "who are you" in user_input:
            return "I am JARVIS, a Just A Rather Very Intelligent System. Your companion and assistant."
        elif "status" in user_input:
            return "All systems are functioning within normal parameters, Sir."
        elif "help" in user_input:
            return "I can assist with system commands, web searches, or simply engage in conversation. What do you require?"
        else:
            return "I'm sorry Sir, I'm currently operating in limited mode without my full neural network connection. However, I will do my best to assist."
