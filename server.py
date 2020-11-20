from flask import Flask, request, abort
from update_json import updater
import admin
import traceback

from wechatpy.crypto import WeChatCrypto
from wechatpy import parse_message, create_reply, replies
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.exceptions import InvalidAppIdException

WECHAT_TOKEN = "rayneNB"
ENCODING_AESKEY = "S8PNVvWvjWeEHLkxXQsPuAOwiBob3lFBgyWj9ppH2TL"
APPID = 'wx76446f9d1e23ea1e'

app = Flask(__name__)
subscribe_message = "欢迎使用长大疫情自动填报系统。\n" \
                    "可回复“我要打卡”查看使用方式。\n" \
                    "可回复“安全承诺”查看安全性\n" \
                    "可回复“原理”获取打卡机制。" \
                    "\n" \
                    "本系统非官方发布，仅供学习参考。\n" \
                    "个人开发者制作，欢迎留言讨论\n" \
                    "生命不息，折腾不止"


@app.route('/wechat', methods=["GET", "POST"])
def wechat():
    try:
        """对接微信公众号服务器"""
        signature = request.args.get("signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echo_str = request.args.get("echostr")
        msg_signature = request.args.get("msg_signature")

        # get和post都需要验证身份
        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            abort(403)

        if request.method == "GET":
            return echo_str

        else:  # POST
            crypto = WeChatCrypto(WECHAT_TOKEN, ENCODING_AESKEY, APPID)
            # 解密
            try:
                msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
                msg = parse_message(msg)
            except (InvalidSignatureException, InvalidAppIdException):  # 解密错误
                abort(403)

            # msg已经为解构的消息
            if msg.type == "text":
                # 功能和彩蛋
                logo = {"宋圆圆": replies.ImageReply(type='image', media_id='76bEgrqnVx638NHtgdYBi8QJfzcjNdYliT1U6WNc28M',
                                                  message=msg),
                        "宋文艳": '爱你哟宝贝~',
                        "author": "Rayne",
                        "count": admin.getAccount_num(),
                        "我要打卡": admin.Introduce,
                        "安全承诺": admin.safe_ntro,
                        "原理": admin.HAHA,
                        'error': admin.error_fail.returnError()
                        }
                if logo.get(msg.content) is not None:
                    if isinstance(logo.get(msg.content), replies.ImageReply):  # 图片
                        msg.type = 'image'
                        reply = logo.get(msg.content)
                    else:
                        reply = create_reply(str(logo.get(msg.content)), msg)  # str

                else:
                    reply = create_reply(str(updater(strs=msg.content)), msg)

            elif msg.type == "event":  # 事件
                if msg.event == 'subscribe':
                    reply = create_reply(subscribe_message, msg)
                else:
                    reply = create_reply(msg.event, msg)
            # 将字典转换为xml字符串
            elif msg.type == "image":
                reply = replies.ImageReply(type='image', media_id='76bEgrqnVx638NHtgdYBi1ag-GqEmvYWIyDAcRUU8Q4',
                                           message=msg)
            else:
                reply = create_reply('非法信息', msg)
            # 返回消息数据给微信服务器
            return crypto.encrypt_message(reply.render(), nonce, timestamp)
    except:
        admin.error_fail.errorOccur()
        print('ERROR')
        print(traceback.format_exc())


app.run(host='0.0.0.0', port=80, threaded=True)
