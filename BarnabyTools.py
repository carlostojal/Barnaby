
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

        nltk.download('punkt')
        nltk.download('wordnet')

        self.sent_tokens = nltk.sent_tokenize(raw)
        self.word_tokens = nltk.word_tokenize(raw)

    def greeting(self, sentence):
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)
    
    def weather(self, sentence):
        for word in sentence.split():
            if word.lower() in WEATHER_INPUTS:
                city_in_sentence = False
                # searches city in user sentence
                URL = "https://api.openweathermap.org/data/2.5/weather"
                for city_search in sentence.split():
                    PARAMS = {
                        'apikey': 'c9f1d2a6eaec5f917473c187547ba288',
                        'q': city_search,
                        'units': 'metric'
                    }
                    r = requests.get(url = URL, params = PARAMS)
                    data = r.json()
                    if data['cod'] == 200:
                        city = data['name']
                        city_in_sentence = True
                        break
                if not city_in_sentence:
                    # gets user city by IP address
                    URL = "https://api.ipgeolocation.io/ipgeo"
                    PARAMS = {
                        'apiKey': '747a7ad91fc84b2b83dff71d9ac0af16',
                    }
                    r = requests.get(url = URL, params = PARAMS)
                    city = r.json()['city']

                    URL = "https://api.openweathermap.org/data/2.5/weather"
                    for city_search in sentence.split():
                        PARAMS = {
                            'apikey': 'c9f1d2a6eaec5f917473c187547ba288',
                            'q': city,
                            'units': 'metric'
                        }
                        r = requests.get(url = URL, params = PARAMS)
                        data = r.json()

                # returns response to user
                output = "It's " + str(data['main']['temp']) + "ºC, " + data['weather'][0]['description'] + " in " + data['name']
                if not city_in_sentence:
                    output += " (I think it's your location)."
                else:
                    output += "."
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
