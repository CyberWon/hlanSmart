# -*- coding:utf-8 -*-  
from cores.flask import Flask
from flask_sockets import Sockets
from cores.wsrpc.rpc import rpc_ws
from cores import logger
app = Flask(__name__)
app.debug=True
sockets = Sockets(app)
ws_list=[]
@sockets.route('/ws')
def echo_socket(ws):
    ws_list.append(ws)
    try:
        while not ws.closed:
            message = ws.receive()
#             print message
            ws.send(rpc_ws(message,ws))
#             print rpc_ws(message,ws)
    except Exception as e:
        print e
@app.route('/')
def hello():
    return 'Hello World!'
@app.route('/test_ws')
def test_ws():
    for i in ws_list:
        i.send('test')
    return ''
if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever() 