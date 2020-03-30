
import json
from neural_network import NeuralNetwork

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
        q = q.lower()
        response = {}
        neuralnetwork = NeuralNetwork(self.config)
        response['functionality'] = neuralnetwork.predict(q, train)
        return json.dumps(response)

