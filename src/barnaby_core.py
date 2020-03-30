
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# barnaby_core.py
#

# Manages Barnaby core configurations

import json

class BarnabyCore:
    def __init__(self):
        self.api_config = self.get_api_config()
         
    def get_api_config(self): # gets api configuration from file 'config/api.json'
        f = open("../config/api.json", "r")
        config = json.loads(f.read())
        f.close()
        # convert data types
        config['server']['port'] = int(config['server']['port'])
        config['server']['debug']  = (config['server']['debug'] == "true")
        # updates object config attribute and returns
        self.api_config = config
        return config

    def get_api_config_details(self):
        return "Host: {}\nPort: {}\nDebug: {}\nOptions: {}".format(self.api_config['server']['host'], str(self.api_config['server']['port']), str(self.api_config['server']['debug']), self.api_config['server']['options'])
