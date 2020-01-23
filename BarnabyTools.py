
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# BarnabyTools.py
#

import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import speech_recognition as sr
import pyttsx3
import os

from inputs import *
from responses import *

class BarnabyTools:

    sent_tokens = []
    word_tokens = []
    lemmer = nltk.stem.WordNetLemmatizer()
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def __init__(self):
        f = open('barnaby.txt', 'r', errors = 'ignore')

        raw = f.read()

        raw = raw.lower()

        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)

        self.sent_tokens = nltk.sent_tokenize(raw)
        self.word_tokens = nltk.word_tokenize(raw)
    
    def user_exists(self):
        return os.path.exists("user_data.json")

    def input(self):
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                user_response = r.recognize_google(audio)
                return user_response
            except sr.UnknownValueError:
                return "(imperceptible)"

    def output(self, sentence):
        print(sentence)
        engine = pyttsx3.init()
        engine.say(sentence)
        engine.runAndWait()

    def welcome(self):
        return random.choice(GREETING_RESPONSES) + ". " + random.choice(WELCOME_RESPONSES)

    def welcome_back(self, user):
        return random.choice(WELCOME_BACK_RESPONSES) + ", " + user.getName()

    def greeting(self, user):
        return random.choice(GREETING_RESPONSES) + ", " + user.getName()
    
    def goodbye(self, user):
        return random.choice(GOODBYE_RESPONSES) + ", " + user.getName()

    def affirmative(self, user):
        response = random.choice(AFFIRMATIVE_RESPONSES)
        if response == "yes":
            if user.getGenre() == "male":
                response += ", sir"
            else:
                response += ", ma'am"
        return response
    
    def weather(self, sentence):
        # Ex: 
        # how's the weather
        # how's the weather in lisbon
        city_in_sentence = False
        if sentence in WEATHER_INPUTS:
            # gets user city by IP address
            URL = "https://api.ipgeolocation.io/ipgeo"
            PARAMS = {
                'apiKey': '747a7ad91fc84b2b83dff71d9ac0af16',
            }
            r = requests.get(url = URL, params = PARAMS)
            city = r.json()['city']

            URL = "https://api.openweathermap.org/data/2.5/weather"
            PARAMS = {
                'apikey': 'c9f1d2a6eaec5f917473c187547ba288',
                'q': city,
                'units': 'metric'
            }
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()
        elif "in" in sentence.split():
            if sentence.split(" in ")[0] in WEATHER_INPUTS:
                city_search = sentence.split(" in ")[1]
                # searches city in user sentence
                URL = "https://api.openweathermap.org/data/2.5/weather"
                PARAMS = {
                    'apikey': 'c9f1d2a6eaec5f917473c187547ba288',
                    'q': city_search,
                    'units': 'metric'
                }
                r = requests.get(url = URL, params = PARAMS)
                data = r.json()
                if data['cod'] != 200:
                    # gets user city by IP address
                    URL = "https://api.ipgeolocation.io/ipgeo"
                    PARAMS = {
                        'apiKey': '747a7ad91fc84b2b83dff71d9ac0af16',
                    }
                    r = requests.get(url = URL, params = PARAMS)
                    city = r.json()['city']
 
                    URL = "https://api.openweathermap.org/data/2.5/weather"
                    PARAMS = {
                        'apikey': 'c9f1d2a6eaec5f917473c187547ba288',
                        'q': city,
                        'units': 'metric'
                    }
                    r = requests.get(url = URL, params = PARAMS)
                    data = r.json()
                else:
                    city_in_sentence = True

        if 'data' in locals():
            # returns response to user
            output = "It's " + str(data['main']['temp']) + "C, " + data['weather'][0]['description'] + " in " + data['name']
            if not city_in_sentence:
                output += " (I think it's your location)."
            else:
                output += "."
            return output

    def news(self, sentence):
        if sentence in NEWS_INPUTS:
            # gets user country by IP address
            URL = "https://api.ipgeolocation.io/ipgeo"
            PARAMS = {
                'apiKey': '747a7ad91fc84b2b83dff71d9ac0af16',
            }
            r = requests.get(url = URL, params = PARAMS)
            full_country = r.json()['country_name']
            country = r.json()['country_code2']
                
            URL = "https://newsapi.org/v2/top-headlines"
            PARAMS = {
                'apiKey': 'ea061f4b7a9b4d3a9df9025cdbc5b2ae',
                'country': country
            }
            r = requests.get(url = URL, params = PARAMS)
            # print(country)
            data = r.json()
            # print(data)
            output = "Here are the top headlines in " + full_country + " (I think it's your location).\n\n"
            for i in range(3):
                output += "\'" + data['articles'][i]['title'] + "\' - " + data['articles'][i]['source']['name'] + " at " + data['articles'][i]['publishedAt'] + "\n(" + data['articles'][i]['url'] + ")\n\n"
            return output
        
    def search(self, sentence):
        URL = "https://www.googleapis.com/customsearch/v1?key=AIzaSyAw1RSB8i_FET7eiF1SbnzjQvz_jl5y3aA&cx=012615923940155512814:ehd2wi47xev&q=democracy"
        PARAMS = {
            'key': 'AIzaSyAw1RSB8i_FET7eiF1SbnzjQvz_jl5y3aA',
            'cx': '012615923940155512814:ehd2wi47xev',
            'q': sentence
        }
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        output = "I discovered this on the internet.\n\n" + data['items'][0]['title'] + "\n" + data['items'][1]['title'] + "\n" + data['items'][2]['title']
        return output

    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    def response(self, user_response):
        bot_response = ''
        self.sent_tokens.append(user_response)

        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize)
        tfid = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfid[-1], tfid)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfid = flat[-2]

        if(req_tfid==0):
            bot_response = bot_response + "I'm sorry. I don't understand."
            return bot_response
        else:
            bot_response = bot_response + self.sent_tokens[idx]
            return bot_response
