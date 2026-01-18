# core/command_processor.py
import os
import subprocess

def process_command(command: str) -> str:

    command = command.lower()

    # ---------- OPEN CHROME ----------
    if "open chrome" in command or "launch chrome" in command:
        try:
            subprocess.Popen("start chrome", shell=True)
            return "Google Chrome opened successfully."
        except Exception as e:
            return f"Failed to open Chrome: {e}"

    # ---------- OPEN NOTEPAD ----------
    elif "open notepad" in command:
        subprocess.Popen("notepad")
        return "Notepad opened."
    
    elif "open youtube" in command:
        subprocess.Popen("start https://www.youtube.com", shell=True)
        return "Opening YouTube."


    else:
        return "Sorry, I don't know how to do that yet."
