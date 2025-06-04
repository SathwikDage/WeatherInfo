import pyttsx3
import speech_recognition as sr
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    speak("Hello Sir, say 'weather' to get weather info or say 'stop' to exit.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        speak("Listening...")
        try:
            audio = r.listen(source, timeout=10)
            text = r.recognize_google(audio)
            print(f"Recognized text: {text.lower()}")
            return text.lower()
        except sr.RequestError as e:
            speak("There was an error. Please try again later.")
        except Exception as e:
            speak("An unexpected error occurred. Please try again.")
    return ""

def getWeatherInfo():
    r = sr.Recognizer()
    speak("Which city?")
    with sr.Microphone() as source:
        print("Listening for city name...")
        try:
            audio = r.listen(source, timeout=10)
            city = r.recognize_google(audio)
            print("City:", city)
        except:
            speak("Sorry, I did not get the city name.")
            return

    url = f"https://api.weatherapi.com/v1/current.json?key=218f94ca3d394715be4172515242701&q={city}"
    try:
        response = requests.get(url)
        weather_data = json.loads(response.text)
        temperature = weather_data["current"]["temp_c"]
        humidity = weather_data["current"]["humidity"]
        speak(f"The current temperature in {city} is {temperature} degrees Celsius with {humidity} percent humidity.")
    except:
        speak("Sorry, I couldn't fetch the weather information.")

if __name__ == "__main__":
    wish()

    while True:
        command = takeCommand()
        if not command:
            continue

        if "stop" in command:
            speak("Okay, stopping now. Goodbye!")
            break

        elif "weather" in command:
            getWeatherInfo()
            speak("If you want to stop, say 'stop'. Otherwise, say another command.")

        else:
            speak("Sorry, I didn't understand that command. Please try again.")
