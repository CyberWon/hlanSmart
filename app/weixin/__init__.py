# -*- coding:utf-8 -*-

#企业版微信引用库
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.enterprise import parse_message, create_reply

from flask import abort, render_template
from cores import BaseDir
import os,yaml
with open(os.path.join(BaseDir,'conf/weixin.yml')) as f:    
    wx_conf=yaml.load(f)
def app_main(request):
    #获取要设置的微信
    wx_name=request.args.get('wx')
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
        if msg.type == 'text':
            res=msg.content
            reply = create_reply(res, msg).render()
        else:
            reply = create_reply('Can not handle this for now', msg).render()
        res = crypto.encrypt_message(reply, nonce, timestamp)
        return res