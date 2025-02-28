import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import random
import subprocess

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        try:
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
        except sr.RequestError:
            speak("Network error.")
        return None

def get_time():
    speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")

def open_website(command):
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com"
    }
    for site in websites:
        if site in command:
            speak(f"Opening {site}")
            webbrowser.open(websites[site])
            return
    speak("Sorry, I can't open that website.")

def tell_joke():
    speak(random.choice([
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don’t skeletons fight each other? Because they don’t have the guts!"
    ]))

def calculate(expression):
    try:
        result = eval(expression.replace("plus", "+").replace("minus", "-")
                               .replace("times", "*").replace("divided by", "/"))
        speak(f"The answer is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

def run_ollama(command):
    try:
        process = subprocess.Popen(["ollama", "run", "deepseek-r1:1.5b"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)
        output, error = process.communicate(input=command)
        if process.returncode != 0 or not output.strip():
            speak("Sorry, Ollama failed to generate output.")
            return
        speak(output.strip())
    except FileNotFoundError:
        speak("Ollama is not installed or not found in PATH.")
    except Exception:
        speak("An error occurred while running Ollama.")

def main():
    speak("Hello! How can I assist you?")
    while True:
        command = listen()
        if command:
            if "hello" in command:
                speak("Hello! How are you?")
            elif "your name" in command:
                speak("I am your voice assistant.")
            elif "time" in command:
                get_time()
            elif "open" in command:
                open_website(command)
            elif "joke" in command:
                tell_joke()
            elif "calculate" in command:
                speak("Please say the mathematical expression.")
                expression = listen()
                if expression:
                    calculate(expression)
            elif "generate" in command:
                speak("What should I generate?")
                ollama_command = listen()
                if ollama_command:
                    run_ollama(ollama_command)
            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn't understand.")

if __name__ == "__main__":
    main()