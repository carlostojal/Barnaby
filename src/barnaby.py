
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# barnaby.py
#

# Main functionalities

import json
import random
from neural_network import NeuralNetwork
from apis import APIs

class Barnaby:
    
    def __init__(self):
        self.config = self.get_config()

    def get_config(self):
        f = open("../config/barnaby.json", "r")
        config = json.loads(f.read())
        f.close()
        self.config = config
        return config
    
    def interpret(self, q, train):
        from barnaby_core import BarnabyCore
        response = {}
        if q and q != "":
            q = q.lower()
            neuralnetwork = NeuralNetwork(self.config)
            response['lang'] = self.get_config()['lang']
            response['functionality'] = neuralnetwork.predict(q, train) # use the neural network to guess if the input is requesting news, a term definition or weather
            if response['functionality'] == "news":
                response['content'] = APIs().get_news()
                response['response'] = "I chose this one for you: \"{}\"".format(random.choice(response['content'])['title'])
            elif response['functionality'] == "term_definitions":
                response['content'] = APIs().get_term_definition(q)
                if response['content']['Answer'] != "":
                    response['response'] = response['content']['Answer']
                elif response['content']['Abstract'] != "":
                    response['response'] = response['content']['Abstract']
                elif response['content']['AbstractText'] != "":
                    response['response'] = response['content']['AbstractText']
                else:
                    response['response'] = response['content']['RelatedTopics'][0]['Text']
            elif response['functionality'] == "weather":
                response['content'] = APIs().get_weather()
                if BarnabyCore().get_api_config()['weather']['units'] == "metric":
                    units = "C"
                else:
                    units = "F"
                response['response'] = "It's {} and a temperature of {}º{} in {}. I think it's your location.".format(response['content']['weather'][0]['description'], response['content']['main']['temp'], units, response['content']['name'])
        else:
            response['error'] = "'q' parameter is required."
        return response