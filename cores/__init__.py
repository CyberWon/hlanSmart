# -*- coding:utf-8 -*-
import json,yaml,os,logging,logging.config
BaseDir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.config.fileConfig(os.path.join(BaseDir,"conf/logger.ini"))
logger = logging.getLogger("hlanSmart")
with open(os.path.join(BaseDir,"conf/hlan.yml")) as f:
    config=yaml.load(f)

with open(os.path.join(BaseDir,'languages/zh_CN.yml')) as f:
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
if __name__=='__main__':
    pass

        