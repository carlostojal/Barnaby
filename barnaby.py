
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# barnaby.py
#

from BarnabyTools import *

barnabyTools = BarnabyTools()

flag = True
print("\nBarnaby: My name is Barnaby. You can talk to me. To exit, say bye.")

while(flag == True):
    print("")
    user_response = input("You: ")
    user_response = user_response.lower()
    if(user_response != "bye"):
        if(user_response == "thanks" or user_response == "thank you"):
            flag = False
            print("Barnaby: You are welcome")
        else:
            if(barnabyTools.greeting(user_response) != None):
                print("Barnaby: " + barnabyTools.greeting(user_response))
            elif(barnabyTools.weather(user_response) != None):
                print("Barnaby: " + barnabyTools.weather(user_response))
            else:
                print("Barnaby: ", end="")
                print(barnabyTools.response(user_response))
                barnabyTools.sent_tokens.remove(user_response)
    else:
        flag = False
        print("Barnaby: Bye, see you later.")