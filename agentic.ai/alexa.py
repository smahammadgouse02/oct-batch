import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Alexa:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)

        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except Exception:
        return ""

def alexa():
    speak("Hello! I am Alexa, your personal assistant.")

    while True:
        command = listen()

        if not command:
            continue

        if "hello" in command or "hi" in command:
            speak("Hello! How can I help you?")

        elif "your name" in command:
            speak("My name is Alexa.")

        elif "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The current time is " + time)

        elif "date" in command:
            date = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is " + date)

        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "open github" in command:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")

        elif "how are you" in command:
            speak("I am fine. Thank you!")

        elif "joke" in command:
            jokes = [
                "Why did the computer get cold? It left its Windows open!",
                "Why do programmers prefer dark mode? Because light attracts bugs!"
            ]
            speak(random.choice(jokes))

        elif "stop" in command or "exit" in command or "goodbye" in command:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I don't know that command yet.")

if __name__ == "__main__":
    alexa()   

    