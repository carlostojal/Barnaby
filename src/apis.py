
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# apis.py
#

# Makes use of the APIs that get the content

import json
import requests
from newsapi import NewsApiClient

class APIs:

    # get APIs URL and keys
    def get_apis_info(self):
        f = open("../config/apis.json", "r")
        apisinfo = json.loads(f.read())
        f.close()
        return apisinfo

    # get user location from IP adress
    def get_location(self):
        url = self.get_apis_info()['geolocation']['url']
        params = {
            "apiKey": self.get_apis_info()['geolocation']['key']
        }
        r = requests.get(url = url, params = params)
        return r.json()

    # get the top headlines for the user contry (from IP) and language defined in Barnaby config file
    def get_news(self):
        from barnaby import Barnaby
        from barnaby_core import BarnabyCore
        newsapi = NewsApiClient(api_key = self.get_apis_info()['news']['key'])
        news = newsapi.get_top_headlines(language = Barnaby().get_config()['lang'].lower(),
                                    country = self.get_location()['country_code2'].lower())
        response = {}
        for i in range(int(BarnabyCore().get_api_config()['news']['number_of_headlines'])):
            if i == len(news['articles']): # if will exceed number of articles
                return response
            response[i] = news['articles'][i]
        return response

    def get_term_definition(self, q):
        from barnaby_core import BarnabyCore
        term = q.split()[len(q.split()) - 1]
        url = self.get_apis_info()['term_definitions']['url']
        params = {
            "q": term,
            "format": BarnabyCore().get_api_config()['term_definitions']['format']
        }
        r = requests.get(url = url, params = params)
        print("{}?q={}".format(self.get_apis_info()['term_definitions']['url'], term))
        return r.json()
    
    # get weather for the user city (from IP)
    def get_weather(self):
        from barnaby import Barnaby
        from barnaby_core import BarnabyCore
        url = self.get_apis_info()['weather']['url']
        params = {
            "q": self.get_location()['city'],
            "units": BarnabyCore().get_api_config()['weather']['units'],
            "lang": Barnaby().get_config()['lang'],
            "appid": self.get_apis_info()['weather']['key']
        }
        r = requests.get(url = url, params = params)
        return r.json()
