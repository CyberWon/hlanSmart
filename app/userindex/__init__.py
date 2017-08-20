#coding=utf-8
from jinja2 import Environment,PackageLoader

def app_main(*args,**kwargs):

    env=Environment(loader=PackageLoader('app.userindex','templates'))
    css=[u'http://static.shuaibo.wang/1.1.0/fonts/font-awesome/font-awesome.css', u'http://static.shuaibo.wang/1.1.0/fonts/web-icons/web-icons.css'] 
    js=[u'http://static.shuaibo.wang/1.1.0/vendor/jquery/jquery.min.js'] 
    exec_js_fun=[u'alert("test")']

    template=env.get_template('index.html')
    return template.render(css=css,js=js,exec_js_fun=exec_js_fun)