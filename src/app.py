
from flask import Flask
from flask import request
import json
from barnaby_core import BarnabyCore
from barnaby import Barnaby

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/api_config")
def api_config():
    return json.dumps(barnabycore.api_config, indent=4)

@app.route("/assistant", methods=['GET'])
def assistant():
    q = request.args.get('q')
    train = (request.args.get('train') == "true")
    return assistant.interpret(q, train)

assistant = Barnaby()

barnabycore = BarnabyCore()

print(barnabycore.get_api_config_details() + "\n")

app.run(barnabycore.api_config['host'], barnabycore.api_config['port'], barnabycore.api_config['debug'], barnabycore.api_config['options'])
