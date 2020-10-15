import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
import string

from lxml import html
from googlesearch import search
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#engine.getProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am your virtual assistant. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
         print("Listening...")
         audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in') 
        print("You said: ",query)
    except Exception as e:
        print("Didn't recognize it. Please say that again.")
        return "None"
    return query

def chatbot_query(query, index=0):
    fallback = 'Sorry, I cannot think of a reply for that.'
    result = ''

    try:
        search_result_list = list(search(query, tld="co.in", num=10, stop=3, pause=1))

        page = requests.get(search_result_list[index])

        tree = html.fromstring(page.content)

        soup = BeautifulSoup(page.content, features="lxml")

        article_text = ''
        article = soup.findAll('p')
        for element in article:
            article_text += '\n' + ''.join(element.findAll(text = True))
        article_text = article_text.replace('\n', '')
        first_sentence = article_text.split('.')
        first_sentence = first_sentence[0].split('?')[0]

        chars_without_whitespace = first_sentence.translate(
            { ord(c): None for c in string.whitespace }
        )

        if len(chars_without_whitespace) > 0:
            result = first_sentence
        else:
            result = fallback

        return result
    except:
        if len(result) == 0: result = fallback
        return result

def exit_program():
    speak('Have a good day!')
    exit()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        #using wikipedia to answer
        if 'wikipedia' in query:
            speak("Searching wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        
        #exceptional questions or queries
        elif 'how are you' in query:
            speak("I am great. Thanks for asking!")
        
        elif 'your name' in query:
            speak("My inventor calls me Prototype1")
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        
        elif 'open google' in query:
            webbrowser.open("google.com")
        
        elif 'play music' in query:
            music_dir = 'C:\\Users\\Jayant\\Desktop\\New folder\\Music'
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir,songs[0]))
        
        elif 'time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak("the time is ")
            speak(strtime)
         
        elif 'exit' in query:
            exit_program()
        
        elif 'stop' in query:
            exit_program()

        #using google search to answer queries
        elif 'who is' in query:
            search_result = chatbot_query(query)
            print(search_result)
            speak(search_result)
        
        elif 'what is' in query:
            search_result = chatbot_query(query)
            print(search_result)
            speak(search_result)
        
        else:
            search_result = chatbot_query(query)
            print(search_result)
            speak(search_result)
        
       