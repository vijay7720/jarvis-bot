from input.voice_input import listen
from input.chat_ui import start_chat
from executor.system_tasks import open_app
from executor.file_tasks import create_folder_on_desktop
import threading

def handle_command(text):
    if not text:
        return

    text = text.lower()
    print("Command:", text)

    if "open chrome" in text:
        open_app("chrome")

    elif "create folder" in text:
        create_folder_on_desktop("C:/Users/vijay/Documents/Deepak/NewFolder")

    else:
        print("Command not recognized")

def voice_loop():
    while True:
        text = listen()
        handle_command(text)

# Run voice listener in background
threading.Thread(target=voice_loop, daemon=True).start()

# Start chat UI
start_chat(handle_command)