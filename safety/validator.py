ALLOWED_ACTIONS = ["open_app", "create_folder"]

def is_allowed(action):
    return action in ALLOWED_ACTIONS
