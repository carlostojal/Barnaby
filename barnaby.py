
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# barnaby.py
#

from BarnabyTools import *

barnabyTools = BarnabyTools()
r = sr.Recognizer()
mic = sr.Microphone()

flag = True

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

print("")

print("Barnaby: ", end="")
barnabyTools.output("Hi, my name is Barnaby. I'm your personal assistant. You can talk to me. To exit, say bye.\n")

while(flag == True):
    print("You: ")
    user_response = ""
    # user_response = input("You: ")
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        user_response = r.recognize_google(audio)
        print(user_response)
    except sr.UnknownValueError:
        continue
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
    print("")