import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  
import pyttsx3
import speech_recognition as sr

# Initialize OpenAI API with your API key

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen_for_wake_word(wake_word="alice"):
    """Continuously listens for the wake word"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:
        with mic as source:
            print("Listening for wake word...")
            audio = recognizer.listen(source)
            try:
                # Recognize the audio using Google Web Speech API
                phrase = recognizer.recognize_google(audio).lower()
                print(f"Detected phrase: {phrase}")

                if wake_word in phrase:
                    speak("Yes, how can I help you?")
                    return True
            except sr.UnknownValueError:
                # Could not understand the audio
                continue
            except sr.RequestError:
                # Service is down
                speak("Sorry, my speech service is down.")
                return False

def listen():
    """Listens for user input after wake word is detected"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"User said: {user_input}")
            return user_input
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None

def ask_openai(question):
    """Queries OpenAI with the given question using the updated API"""
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # Or "gpt-4" if you're using GPT-4
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question},
    ])
    answer = response.choices[0].message.content
    return answer

def main():
    """Main function to start Alice"""
    speak("Hello, I am Alice, your virtual assistant. Say 'Alice' to activate me.")

    while True:
        if listen_for_wake_word():
            user_input = listen()
            if user_input:
                if "exit" in user_input.lower() or "stop" in user_input.lower():
                    speak("Goodbye!")
                    break
                response = ask_openai(user_input)
                speak(response)

if __name__ == "__main__":
    main()
