# -*- coding:utf-8 -*-
import json,yaml
with open('languages/zh_CN.yml') as f:
    lang=yaml.load(f)
# print lang
def getLang(num):
#     print num
    return lang.get(num)
def WS_SEND(WS_OBJECT,SEND_DATA):
    try:
        WS_OBJECT.get('_ws').send(json.dumps(dict(
            retFun=WS_OBJECT.get('request'),
            retData=SEND_DATA
            )))
    except Exception as e:
        print ''
        