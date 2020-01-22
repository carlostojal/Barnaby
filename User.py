
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# User.py
#

import json

class User:

    name = ""
    genre = ""

    def __init__(self):
        self.name = ""
        self.genre = ""

    def loadUser(self):
        f = open("user_data.json", "r")
        user_data = json.load(f)
        self.setName(user_data['name'])
        self.setGenre(user_data['genre'])
        return user_data

    def saveUser(self, user):
        f = open("user_data.json", "w")
        f.write(json.dumps(user))
        f.close()

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getGenre(self):
        return self.genre

    def setGenre(self, genre):
        self.genre = genre