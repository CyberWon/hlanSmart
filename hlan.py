# -*- coding:utf-8 -*-  
from cores.flask import Flask,request,jsonify
from flask_sockets import Sockets
from cores.wsrpc.rpc import rpc_ws
from cores import logger,config,getLang
import sys
app = Flask(__name__)
app.debug=True
sockets = Sockets(app)
ws_list=[]
@app.route('/app/<app_name>',methods=['GET','POST'])
def apps(app_name):
    try:
        app_str='app.%s' % app_name
        if config['debug']==True:
            try:
                del sys.modules[app_str]
            except:
                pass
        method=__import__(app_str,fromlist=["app_main"]) 
    except:
        return jsonify(dict(retfun='print',retdata=getLang(1000003)))
    try:
        ret=method.app_main(request)
        return ret
    except:
        return jsonify(dict(retfun='print',retdata=getLang(1000004)))
@sockets.route('/ws')
def echo_socket(ws):
    ws_list.append(ws)
    ip = request.remote_addr  
    try:
        _ip = request.headers["X-Real-IP"]
        if _ip is not None:
            ip = _ip
    except Exception as e:
        logger.debug(e)
    try:
        while not ws.closed:
            message = ws.receive()
            logger.info('%s %s'%(ip,message))
            ws.send(rpc_ws(message,ws))
    except Exception as e:
        logger.debug(e)
@app.route('/')
def hello():
    return 'HlanSmart v0.1!'
if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever() 