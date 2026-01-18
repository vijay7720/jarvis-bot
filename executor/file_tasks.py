import os

def create_folder_on_desktop(folder_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    print(f"📁 Folder created at: {folder_path}")
