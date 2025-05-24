import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import time
import traceback

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapikey = "979aa5d9ffbf4650b0af7e7080cf8dc4"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    try:
        # Generate and save MP3
        tts = gTTS(text)
        tts.save("temp.mp3")

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()

        # Wait for the audio to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Small delay to ensure file release
        time.sleep(0.5)

    except Exception as e:
        print(f"Error in speak(): {e}")

    finally:
        # Delete temp file safely
        try:
            if os.path.exists("temp.mp3"):
                os.remove("temp.mp3")
        except Exception as e:
            print(f"Failed to delete temp.mp3: {e}")

def aiProcess(command):
    client = OpenAI(api_key="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",
)
    completion = client.chat.completions.create( 
    model = "gpt-3.5-turbo", 
    messages =[
        {"role": "system", "content": "You are a virtual assistant named jarvis..."},
        {"role": "user", "content":command}
    ]
    )
    return print(completion.choices[0].message.content)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        
    elif "open you tube" in c.lower():
        webbrowser.open("https://youtube.com")
    
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapikey}")
        if r.status_code == 200:
        #Parse the JSON response 
            data = r.json() 
        #Extract the articles 
            articles = data.get('articles', []) 
        #Print the headlines 
        for article in articles: 
            speak(article['title'])

        else:
            #Let OpenAI handle the rquest 
            output = aiProcess(c)     



if __name__ == "__main__": 
    speak("Initializing Jarvis...")
    while True:
        #Listen for the wake word jarvis
        #Obtain audio from microphone
        r = sr. Recognizer() 
        
        #recognize speech using google
        print("Recognizing") 
        try: 
            with sr.Microphone() as source: 
                print("Listening") 
                audio = r.listen(source , timeout = 5 , phrase_time_limit = 3)
            word =  r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yaa")
                #Listen for command

                with sr.Microphone() as source: 
                   print("Jarvis Activated...") 
                   audio = r.listen(source)
                   command =  r.recognize_google(audio)

                   processCommand(command)

        except Exception as e:
            traceback.print_exc()
