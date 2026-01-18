# input/voice_input.py
import speech_recognition as sr

def listen_from_mic():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except sr.UnknownValueError:
        return "sorry, i did not understand"
    except sr.RequestError:
        return "speech service unavailable"
