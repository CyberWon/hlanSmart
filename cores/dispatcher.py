# -*- coding:utf-8 -*-  
""" Dispatcher is used to add methods (functions) to the server.

For usage examples see :meth:`Dispatcher.add_method`

"""
import collections,sys,json,os,yaml
from cores import config,logger,BaseDir
from flask import abort
with open(os.path.join(BaseDir,'conf/weixin.yml')) as f:    
    wx_conf=yaml.load(f)
def ent_weixin(wx_name=None):
    def _app_weixin(func):
        def __app_weixin(request):
            from wechatpy.enterprise.crypto import WeChatCrypto
            from wechatpy.exceptions import InvalidSignatureException
            from wechatpy.enterprise.exceptions import InvalidCorpIdException
            from wechatpy.enterprise import parse_message, create_reply
            TOKEN=wx_conf[wx_name]['TOKEN']
            EncodingAESKey=wx_conf[wx_name]['EncodingAESKey']
            AppId=wx_conf[wx_name]['AppId']
            signature = request.args.get('msg_signature', '')
            timestamp = request.args.get('timestamp', '')
            nonce = request.args.get('nonce', '')
            crypto = WeChatCrypto(TOKEN, EncodingAESKey, AppId)
            if request.method == 'GET':
                echo_str = request.args.get('echostr', '')
                try:
                    echo_str = crypto.check_signature(
                        signature,
                        timestamp,
                        nonce,
                        echo_str
                    )
                except InvalidSignatureException:
                    abort(403)
                return echo_str
            else:
                try:
                    msg = crypto.decrypt_message(
                        request.data,
                        signature,
                        timestamp,
                        nonce
                    )
                except (InvalidSignatureException, InvalidCorpIdException):
                    abort(403)
                msg = parse_message(msg)
                reply = create_reply(func(msg), msg).render()
                res = crypto.encrypt_message(reply, nonce, timestamp)
                return res
        return __app_weixin
    return _app_weixin
def hlan_app(auth=False):
    def _hlan_app(func):
        def __hlan_app(request):
            #将请求的参数转换成字典
            try:
                if request.method == 'GET':
                    d=request.args.to_dict()
                else:
                    d=request.form.to_dict()
            except Exception as e:
                logger.error(e)
                
            #获取请求参数中的方法   
            m=d['method'].split('.')
            mod_str=str(request.path).replace('/', '.')[1:]+'.'+m[0]
            #如果开启认证，在这里判断是否拦截请求。
            if auth:
                pass
            try:
                #是否重新加载模块.
                if config['debug']==True:
                    try:
                        del sys.modules[mod_str]
                    except:
                        pass
                method=__import__(mod_str,fromlist=["MD"])
            except Exception as e:
                logger.error(e)
            try:
                res=method.MD[m[1]]
                try:
                    d['params']=json.loads(d.get('params'))
                except:
                    pass
                return json.dumps(dict(id=d.get('id'),retfun=d.get('retfun'),retdata=res(args=d)))
            except Exception as e:
                logger.error(e)
                return json.dumps(dict(id=d.get('id'),retfun=d.get('retfun'),retdata=""))
        return __hlan_app
    return _hlan_app
class Dispatcher(collections.MutableMapping):

    """ Dictionary like object which maps method_name to method."""

    def __init__(self, prototype=None):
        """ Build method dispatcher.

        Parameters
        ----------
        prototype : object or dict, optional
            Initial method mapping.

        Examples
        --------

        Init object with method dictionary.

        >>> Dispatcher({"sum": lambda a, b: a + b})
        None

        """
        self.method_map = dict()

        if prototype is not None:
            self.build_method_map(prototype)

    def __getitem__(self, key):
        return self.method_map[key]

    def __setitem__(self, key, value):
        self.method_map[key] = value

    def __delitem__(self, key):
        del self.method_map[key]

    def __len__(self):
        return len(self.method_map)

    def __iter__(self):
        return iter(self.method_map)

    def __repr__(self):
        return repr(self.method_map)

    def add_class(self, cls):
        prefix = cls.__name__.lower() + '.'
        self.build_method_map(cls(), prefix)

    def add_object(self, obj):
        prefix = obj.__class__.__name__.lower() + '.'
        self.build_method_map(obj, prefix)

    def add_dict(self, dict, prefix=''):
        if prefix:
            prefix += '.'
        self.build_method_map(dict, prefix)

    def add_method(self, f, name=None):
        """ Add a method to the dispatcher.

        Parameters
        ----------
        f : callable
            Callable to be added.
        name : str, optional
            Name to register (the default is function **f** name)

        Notes
        -----
        When used as a decorator keeps callable object unmodified.

        Examples
        --------

        Use as method

        >>> d = Dispatcher()
        >>> d.add_method(lambda a, b: a + b, name="sum")
        <function __main__.<lambda>>

        Or use as decorator

        >>> d = Dispatcher()
        >>> @d.add_method
            def mymethod(*args, **kwargs):
                print(args, kwargs)

        """
        self.method_map[name or f.__name__] = f
        return f

    def build_method_map(self, prototype, prefix=''):
        """ Add prototype methods to the dispatcher.

        Parameters
        ----------
        prototype : object or dict
            Initial method mapping.
            If given prototype is a dictionary then all callable objects will
            be added to dispatcher.
            If given prototype is an object then all public methods will
            be used.
        prefix: string, optional
            Prefix of methods

        """
        if not isinstance(prototype, dict):
            prototype = dict((method, getattr(prototype, method))
                             for method in dir(prototype)
                             if not method.startswith('_'))

        for attr, method in prototype.items():
            if callable(method):
                self[prefix + attr] = method
