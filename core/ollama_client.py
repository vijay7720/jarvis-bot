import subprocess
import json
import re

OLLAMA_MODEL = "llama3"

SYSTEM_PROMPT = """
You are a command parser.

STRICT RULES:
- Respond with ONLY valid JSON
- Do NOT explain
- Do NOT add text
- Do NOT use markdown

JSON format:
{
  "action": "<open_app | open_website | unknown>",
  "target": "<string or null>"
}

Examples:
User: open chrome
Response: {"action":"open_app","target":"chrome"}

User: open google.com
Response: {"action":"open_website","target":"google.com"}

User: hello
Response: {"action":"unknown","target":null}
"""

def ask_ollama(user_input: str) -> dict:
    prompt = f"{SYSTEM_PROMPT}\nUser: {user_input}\nResponse:"

    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        raw = result.stdout.decode("utf-8", errors="ignore")

        # 🔥 Extract JSON even if extra text exists
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())

        print("⚠ Ollama returned no JSON:", raw)
        return {"action": "unknown", "target": None}

    except Exception as e:
        print("❌ Ollama failure:", e)
        return {"action": "unknown", "target": None}
