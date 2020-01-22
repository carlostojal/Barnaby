
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
    barnabyTools.output("Please answer directly, don't give complete answers.")
    print("Barnaby: ", end="")
    barnabyTools.output("What's your name?")
    user.setName(input("You: "))
    print("Barnaby: ", end="")
    while user.getGenre() != "male" and user.getGenre() != "female":
        barnabyTools.output("What's your genre (Male/Female)?")
        user.setGenre(input("You: ").lower())
    user1 = {
        'name': user.getName(),
        'genre': user.getGenre()
    }
    user.saveUser(user1)
    user.loadUser()
    barnabyTools.output(barnabyTools.welcome() + ", " + user.getName())

user.loadUser()
barnabyTools.output(barnabyTools.welcome_back(user))

while(flag == True):
    # print("You: ")
    user_response = ""
    user_response = input("You: ")
    '''
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        user_response = r.recognize_google(audio)
        print(user_response)
    except sr.UnknownValueError:
        print("(imperceptible)")
        continue
    '''
    user_response = user_response.lower()
    if(user_response != "bye"):
        print("Barnaby: ", end="")
        print("typing...", end="")
        if(user_response == "thanks" or user_response == "thank you"):
            flag = False
            barnabyTools.output("You're welcome.")
        else:
            if(barnabyTools.greeting(user_response) != None):
                barnabyTools.output(barnabyTools.greeting(user_response))
            elif(barnabyTools.news(user_response) != None):
                barnabyTools.output(barnabyTools.news(user_response))
            elif(barnabyTools.weather(user_response) != None):
                barnabyTools.output(barnabyTools.weather(user_response))
            else:
                barnabyTools.output(barnabyTools.response(user_response))
                barnabyTools.sent_tokens.remove(user_response)
    else:
        flag = False
        print("Barnaby: ", end="")
        barnabyTools.output("Bye, see you later.")