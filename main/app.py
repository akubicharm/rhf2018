import os
import json
import datetime
import random
import time
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, render_template

app = Flask(__name__)

ws_list = set()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/publish')
def publish():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        ws_list.add(ws)

        while True:
            msg = ws.receive()
            if msg is None:
                break
            print(msg)
            for s in ws_list:
                s.send(msg)

        # while True:
        #    t = int(time.mktime(datetime.datetime.now().timetuple()))
        #    ws.send(json.dumps([{"time": t, "y": random.random() * 1000},
        #                        {"time": t, "y": random.random() * 1000}]))
        #    time.sleep(1)
    return


@app.route('/sendmsg', methods=['GET', 'POST'])
def sendmsg():
    if request.method == "GET":
        return """
        GET IS NOT AVAILABLE
        """
    else:
        print json.dumps(request.json)
        for s in ws_list:
            s.send(json.dumps(request.json))
            """
            t = int(time.mktime(datetime.datetime.now().timetuple()))
            msg = json.dumps([{"time": t, "y": random.random() * 1000},
                              {"time": t, "y": random.random() * 1000}])
            print msg
            s.send(msg)
            """
        return "OK"
    return "OK"


if __name__ == '__main__':
    app.debug = True
    server = pywsgi.WSGIServer(("", 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
