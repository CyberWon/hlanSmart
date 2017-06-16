# -*- coding:utf-8 -*-  
from cores.jsonrpc import Dispatcher
from cores import WS_SEND
_method=Dispatcher()
def ext_main(*args,**kwargs):
    try:
        method=_method.get(kwargs.get('request'))
    except Exception as e:
        if kwargs.get('_ws'):
            WS_SEND(kwargs, e)
        else:
            return e
if __name__=='__main__':
    
    pass