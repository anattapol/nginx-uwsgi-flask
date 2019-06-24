from flask import Flask, request, jsonify
from tornado import httpclient
import time

app = Flask(__name__)


@app.route('/')
def hello_world():
    return """
        Simple response from Flask running inside uWSGI, 
        which is running within nGINX, 
        which is hosted inside a Docker image!
    """


@app.route('/echo_request')
def echo_request():
    return jsonify(dict(request.headers))

@app.route('/sleep')
def sleep():
    time.sleep(65)
    return 'I am awake!!, after slept for 65 seconds'

@app.route('/tornado_20')
def tornado_notimeout():
    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch(httpclient.HTTPRequest(url="http://localhost:8080/sleep"))
        return response.body
    except Exception as e:
        return e
    else:
        return 'else from tornado request'

@app.route('/tornado_70')
def tornado():
    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch(httpclient.HTTPRequest(url="http://localhost:8080/sleep",request_timeout=70))
        return response.body
    except Exception as e:
        return e
    else:
        return 'else from tornado request'
    

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080
    )