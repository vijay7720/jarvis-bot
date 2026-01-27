import subprocess

ALIASES = {
    "vs code": "code",
    "vscode": "code",
    "chrome": "chrome",
    "browser": "chrome"
}

def open_app(app_name: str) -> bool:
    app = ALIASES.get(app_name.lower(), app_name)
    try:
        subprocess.Popen(f"start {app}", shell=True)
        return True
    except:
        return False
