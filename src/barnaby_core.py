
import json

class BarnabyCore:
    def __init__(self):
        self.api_config = self.get_api_config()
         
    def get_api_config(self): # gets api hostname, port, debug and options from 'config/api.json'
        f = open("../config/api.json", "r")
        config = json.loads(f.read())
        f.close()
        # convert data types
        config['port'] = int(config['port'])
        config['debug']  = (config['debug'] == "true")
        # updates object config attribute and returns
        self.api_config = config
        return config

    def get_api_config_details(self):
        return "Host: {}\nPort: {}\nDebug: {}\nOptions: {}".format(self.api_config['host'], str(self.api_config['port']), str(self.api_config['debug']), self.api_config['options'])
