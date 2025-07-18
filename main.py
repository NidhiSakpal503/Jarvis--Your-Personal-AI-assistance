import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "1c94514a743b492cb1ecefeae8ee1407"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

    

def aiProcess(command):
    client = OpenAI(api_key="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"
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role":"system","content":"You are a virtual Assistant Named Jarvis.Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return(completion.choices[0].message.content);

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/feed/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "News" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            #Parse the Json response
            data = r.json()
            #extract the article
            articles = data.get('articles',[])
            #Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        #Let open AI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ =="__main__":
    speak("Initializing Jarvis.....")
    while True:
    #Listen for the wake word Jarvis
    #Obtain Audio from the microphone
        r = sr.Recognizer()
    #recogninize speech using Google
        print("Recognizing......")
        try:
            with sr.Microphone() as source:
                print("Listening.....")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word = r.recognize_google(audio)
        
            if (word.lower()=="jarvis"):
                speak("Ya")
        #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active.....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
    
        except Exception as e:
            print("Error;{0}".format(e))