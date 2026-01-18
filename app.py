from input.voice_input import listen
from input.chat_ui import JarvisUI
from executor.system_tasks import open_app
from executor.file_tasks import create_folder_on_desktop
import threading
import time


ui = None


def handle_command(text):
    if not text:
        return


    text = text.lower()


    if "open chrome" in text:
        ui.add_message("⚙️ Executing: Open Chrome")
        open_app("chrome")
        ui.add_message("✅ Done: Chrome opened")


    elif "create folder" in text:
        ui.add_message("⚙️ Executing: Create Folder")
        create_folder_on_desktop("NewFolder")
        ui.add_message("✅ Done: Folder created")


    else:
        ui.add_message("❌ Sorry, I didn’t understand that")


    ui.set_status("🎤 Listening...")




def voice_loop():
    while True:
        text = listen(ui)
        handle_command(text)
        time.sleep(0.5)


ui = JarvisUI(handle_command)
threading.Thread(target=voice_loop, daemon=True).start()
ui.start()