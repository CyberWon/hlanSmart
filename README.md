# 2017年7月12日 星期三

隔了一个月才更新.主要在完善前端部分,前端部分暂时不考虑开源.整个项目开源的只会是底层框架部分.下个版本主要针对websocket和统一认证进行功能性补充.

## 添加了个HTTP功能的装饰器.

在app目录下面,放入python包文件即可
例如:
>/app/testmod/\__init\__.py
/app/testmod/mod1.py
### HTTP
然后在\__init\__.py添加下面代码就行了
```python
from cores.dispatcher import app_test
@app_test
def app_main(request):
    pass
```
在mod1.py中添加能访问到代码
```python
from cores.dispatcher import Dispatcher
MD=Dispatcher()
@MD.add_method
def haha(msg):
    return 'test,haha'
@MD.add_method
def hehe(msg):
    return 'test,hehe'
```
## 验证结果

### GET
访问的url
>wget http://localhost:82/app/test?method=mod1.haha&&id=11

返回
```json
{"retdata": "test,haha", "retfun": null, "id": "11"}
```

### POST

>curl -d 'id=11&&retfun=console.log&&method=mod1.hehe' http://localhost:82/app/test

返回
```json
{
    "retdata": "test,hehe", 
    "retfun": "console.log", 
    "id": "11"
}
```
# 2017年6月19日 星期一

1.增加了app模块(主要对外提供HTTP服务,比如微信的接入),并提供了微信样例

> /app/weixin?wx=wx1

2.优化了日志功能,正常的访问日志在logs/other.log,hlan程序的放在logs/hlan.log.

# 2017年6月18日 星期日

1. 修复了hot-plugging不能使用的bug.

2. 增加了日志功能.

# 2017年6月16日 星期五

1. 自己写了rpc调用部分.

2. 框架目前初具雏形

# 2017年5月26日 星期五

项目启动