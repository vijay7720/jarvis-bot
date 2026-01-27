import random
from core.ollama_client import ask_ollama
from executor.app_launcher import open_app
from executor.web_launcher import open_website

ACK_PHRASES = [
    "Right away.",
    "On it.",
    "Working on that.",
    "As you wish."
]

def rule_based_parse(command: str):
    command = command.lower()

    if command.startswith("open "):
        target = command.replace("open ", "").strip()
        if "." in target:
            return {"action": "open_website", "target": target}
        return {"action": "open_app", "target": target}

    return None


def process_command(command: str) -> dict:
    ack = random.choice(ACK_PHRASES)

    parsed = rule_based_parse(command)
    ai = parsed if parsed else ask_ollama(command)

    action = ai.get("action")
    target = ai.get("target")

    if action == "open_app" and target:
        success = open_app(target)
        if success:
            return {
                "ack": ack,
                "speech": f"Opening {target}.",
                "text": f"{target.capitalize()} launched successfully."
            }
        else:
            return {
                "ack": "Sorry.",
                "speech": f"I couldn't open {target}.",
                "text": f"Failed to open {target}."
            }

    if action == "open_website" and target:
        open_website(target)
        return {
            "ack": ack,
            "speech": f"Opening {target}.",
            "text": f"Website {target} opened."
        }

    return {
        "ack": "Hmm.",
        "speech": "I don't know how to do that yet.",
        "text": "Unknown command."
    }
