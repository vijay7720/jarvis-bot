import subprocess
import json

OLLAMA_MODEL = "llama3"

SYSTEM_PROMPT = """
You are a desktop automation assistant.
Convert user commands into structured JSON.

Supported actions:
- open_app (example: chrome, vscode)
- open_website (example: google.com)
- unknown

Return ONLY valid JSON.
"""

def ask_ollama(user_input: str) -> dict:
    prompt = f"""
{SYSTEM_PROMPT}

User: {user_input}

JSON:
"""

    result = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL],
        input=prompt,
        text=True,
        capture_output=True
    )

    try:
        return json.loads(result.stdout.strip())
    except:
        return {"action": "unknown"}
