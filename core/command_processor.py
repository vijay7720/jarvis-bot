import subprocess
import os
import random

ACK_PHRASES = [
    "Right away.",
    "On it.",
    "Working on that.",
    "As you wish."
]

COMMON_APP_PATHS = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    r"C:\Windows\System32"
]

APP_CACHE = {}

# ---------- APP ALIASES ----------
APP_ALIASES = {
    "vs code": "code",
    "visual studio code": "code",
    "calculator": "calc",
    "cmd": "cmd",
    "command prompt": "cmd",
    "file explorer": "explorer",
    "explorer": "explorer"
}

# ---------- WEBSITE ALIASES ----------
WEBSITE_ALIASES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "amazon": "https://www.amazon.in",
    "linkedin": "https://www.linkedin.com",
    "chatgpt": "https://chat.openai.com"
}


def find_exe(app_name: str):
    app_name = app_name.lower()

    if app_name in APP_CACHE:
        return APP_CACHE[app_name]

    for base in COMMON_APP_PATHS:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.lower() == f"{app_name}.exe":
                    exe_path = os.path.join(root, file)
                    APP_CACHE[app_name] = exe_path
                    return exe_path

    return None


def process_command(command: str):
    command = command.lower().strip()

    ack = random.choice(ACK_PHRASES)

    if command.startswith("open "):
        target = command.replace("open ", "").strip()

        # Website
        if target in WEBSITE_ALIASES:
            subprocess.Popen(f"start {WEBSITE_ALIASES[target]}", shell=True)
            return {
                "ack": f"{ack} Opening {target}.",
                "result": f"{target.capitalize()} is now open.",
                "success": True
            }

        # App
        app_name = APP_ALIASES.get(target, target)

        try:
            subprocess.Popen(f"start {app_name}", shell=True)
            return {
                "ack": f"{ack} Opening {target}.",
                "result": f"{target.capitalize()} is ready.",
                "success": True
            }
        except:
            exe_path = find_exe(app_name)
            if exe_path:
                subprocess.Popen(exe_path)
                return {
                    "ack": f"{ack} Opening {target}.",
                    "result": f"{target.capitalize()} is ready.",
                    "success": True
                }

        return {
            "ack": f"I tried opening {target}.",
            "result": f"I couldn't find {target} on your system.",
            "success": False
        }

    return {
        "ack": "Sorry?",
        "result": "I didn't understand that command.",
        "success": False
    }

