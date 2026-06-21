import os
import webbrowser
import subprocess

def open_website(url):
    # Basic URL validation/cleaning could be added here
    webbrowser.open(url)
    return f"Opening {url} for you, Sir."

def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searching Google for {query}, Sir."

def run_command(command):
    # Safety: List of allowed safe commands or a confirmation could be implemented here.
    # For now, we will avoid shell=True to reduce injection risk.
    # We also advise the user that JARVIS requires confirmation for system-level changes.

    # Simple check for potentially dangerous keywords
    dangerous_keywords = ["rm -rf", "format", "> /dev/", ":(){ :|:& };:"]
    if any(kw in command for kw in dangerous_keywords):
        return "I'm sorry Sir, I cannot execute that command as it appears to be potentially destructive."

    try:
        # Split command into args to avoid shell=True where possible
        args = command.split()
        result = subprocess.run(args, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return f"Executed command: {command}\nOutput: {result.stdout[:100]}"
        else:
            return f"Command failed with error: {result.stderr[:100]}"
    except Exception as e:
        # Fallback to shell=True for complex commands but with caution
        return f"I'm hesitant to execute that complex command without further verification, Sir. Error: {str(e)}"
