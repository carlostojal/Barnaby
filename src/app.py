
#
# Copyright (c) Carlos Tojal 2020
# Barnaby
# app.py
#

# API Flask server

from flask import Flask
from flask import request
from flask import jsonify
from barnaby_core import BarnabyCore
from barnaby import Barnaby

app = Flask(__name__)

@app.route("/")
def index():
    return assistant.get_readme()

@app.route("/api_config")
def api_config():
    return jsonify(barnabycore.get_api_config())

@app.route("/assistant", methods=['GET'])
def assistant():
    q = request.args.get('q')
    train = (request.args.get('train') == "true")
    return jsonify(assistant.interpret(q, train))

assistant = Barnaby()

barnabycore = BarnabyCore()

print(barnabycore.get_api_config_details() + "\n")

app.run(barnabycore.api_config['server']['host'], barnabycore.api_config['server']['port'], barnabycore.api_config['server']['debug'], barnabycore.api_config['server']['options'])
