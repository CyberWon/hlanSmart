# -*- coding:utf-8 -*-  
import json,sys
from cores import getLang,logger
config={}
config['debug']=True
def rpc_start(message=None,ws=None):
    try:
        mod_str='ext.%s' % message.get('method')
        if config['debug']==True:
            try:
                del sys.modules[mod_str]
            except:
                pass
        method=__import__(mod_str,fromlist=["ext_main"]) 
    except:
        return json.dumps(dict(retfun='print',retdata=getLang(1000003)))
    args=dict(params=message.get('params'),__ws=ws)
    try:
        ret=method.ext_main(args)
        del method
        return ret
    except:
        return json.dumps(dict(retfun='print',retdata=getLang(1000004)))
def rpc_ws(message,ws):
    try:
        message=json.loads(message)
        return rpc_start(message, ws)
    except:
        return json.dumps(dict(retfun='print',retdata=getLang(1000002)))