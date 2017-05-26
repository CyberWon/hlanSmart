# -*- coding:utf-8 -*-  
from flask import Flask

from cores.jsonrpc.backend.flask import api

app = Flask(__name__)
app.add_url_rule('/', 'api', api.as_view())
@api.dispatcher.add_method
def hello(*args, **kwargs):
    return args, kwargs
if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)