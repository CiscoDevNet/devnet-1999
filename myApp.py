#!/usr/bin/env python

from flask import Flask,request
import os
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Cisco LIVE! Barcelona git session"

@app.route("/hostname", methods=['GET'])
def hostname():
  
        return "Not running on Kubernetes POD"

@app.route("/environment", methods=['GET'])
@app.route("/env", methods=['GET'])
def env():
    envs = {}
    for env in os.environ:
        envs[env] = os.environ[env]
    return str(envs)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route("/connect", methods=['GET'])
def connect():
    if request.args['url']:
        response = requests.get(request.args['url'])
    else:
        return "No URL Specified. pass ?url="
    parsed_response = {}
    parsed_response["status"] = response.status_code
    parsed_response["body"] = response.text
    parsed_response["url"] = response.url
    return str(parsed_response)



@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    if "POD_NAME" in os.environ:
        return "Killing POD {}".format(os.environ['POD_NAME'])
    else:
        return "Killing Container {}".format(os.environ['HOSTNAME'])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
