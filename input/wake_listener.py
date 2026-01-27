import speech_recognition as sr
from core.wake_words import WAKE_WORDS

recognizer = sr.Recognizer()

def wait_for_wake_word() -> bool:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print("Wake heard:", text)

        return any(wake in text for wake in WAKE_WORDS)

    except sr.UnknownValueError:
        return False
    except Exception as e:
        print("Wake error:", e)
        return False
