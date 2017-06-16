# -*- coding:utf-8 -*-  
import json
from cores import getLang
def rpc_start(message=None,ws=None):
    try:
        mod_str='ext.%s.ext_main' % message.get('method')
#         method=None
        method=__import__(mod_str,fromlist=True) #
    except:
        return json.dumps(dict(retfun='print',retdata=getLang(1000004)))
    args=dict(params=message.get('params'),__ws=ws)
    try:
        return method.main(args)
    except:
        return json.dumps(dict(retfun='print',retdata=getLang(1000003)))
def rpc_ws(message,ws):
    try:
        message=json.loads(message)
        return rpc_start(message, ws)
    except:
        return json.dumps(dict(retfun='print',retdata=getLang(1000002)))
    