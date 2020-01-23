
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# barnaby.py
#

from BarnabyTools import *
from User import *

barnabyTools = BarnabyTools()
user = User()
r = sr.Recognizer()
mic = sr.Microphone()

flag = True

print("")

print("Weather by OpenWeatherMap API")
print("News by NewsAPI")

print("")

print(" /$$$$$$$                                          /$$                ")
print("| $$__  $$                                        | $$                ")
print("| $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$ | $$$$$$$  /$$   /$$")
print("| $$$$$$$  |____  $$ /$$__  $$| $$__  $$ |____  $$| $$__  $$| $$  | $$")
print("| $$__  $$  /$$$$$$$| $$  \__/| $$  \ $$  /$$$$$$$| $$  \ $$| $$  | $$")
print("| $$  \ $$ /$$__  $$| $$      | $$  | $$ /$$__  $$| $$  | $$| $$  | $$")
print("| $$$$$$$/|  $$$$$$$| $$      | $$  | $$|  $$$$$$$| $$$$$$$/|  $$$$$$$")
print("|_______/  \_______/|__/      |__/  |__/ \_______/|_______/  \____  $$")
print("                                                             /$$  | $$")
print("                                                            |  $$$$$$/")
print("                                                             \______/ ")
print("Developed by Carlos Tojal")

print("")

user = User()
user1 = {}

if not barnabyTools.user_exists():
    barnabyTools.output(barnabyTools.welcome())
    print("Barnaby: ", end="")
    barnabyTools.output("What's your name?")
    # user.setName(input("You: "))
    print("You: ", end="")
    user.setName(barnabyTools.input())
    print(user.getName())
    barnabyTools.affirmative(user)
    while user.getGenre() != "male" and user.getGenre() != "female":
        print("Barnaby: ", end="")
        barnabyTools.output("What's your genre (Male/Female)?")
        # user.setGenre(input("You: ").lower())
        print("You: ", end="")
        user.setGenre(barnabyTools.input())
        print(user.getGenre())
    barnabyTools.affirmative(user)
    user.saveUser()
    barnabyTools.output(barnabyTools.welcome() + ", " + user.getName())
else:
    user.loadUser()
    barnabyTools.output(barnabyTools.welcome_back(user))

while(True):
    user_response = ""
    # user_response = input("You: ")
    user_response = barnabyTools.input()
    user_response = user_response.lower()
    print(user_response)
    if("barnaby" in user_response.split()):
        barnabyTools.output(barnabyTools.greeting(user))
        # user_response = input("You: ")
        user_response = barnabyTools.input()
        user_response = user_response.lower()
        print(user_response)
        print("Barnaby: ", end="")
        barnabyTools.output(barnabyTools.affirmative(user))
        print("Barnaby: typing...")
        if(barnabyTools.news(user_response) != None):
            news = barnabyTools.news(user_response)
            barnabyTools.output(news.split("\n")[0])
            barnabyTools.output(news.split("\n")[2].split(" - ")[0])
            barnabyTools.output(news.split("\n")[5].split(" - ")[0])
            barnabyTools.output(news.split("\n")[8].split(" - ")[0])
            # barnabyTools.output(barnabyTools.news(user_response))
        elif(barnabyTools.weather(user_response) != None):
            barnabyTools.output(barnabyTools.weather(user_response))
        else:
            barnabyTools.output(barnabyTools.response(user_response))
            barnabyTools.sent_tokens.remove(user_response)
        barnabyTools.output(barnabyTools.goodbye(user))