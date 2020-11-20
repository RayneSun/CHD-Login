import json

class error_log(object):
    def __init__(self):
        self.error='无错误触发\n'
        self.sign_fail='无人签到失败'
    def errorOccur(self):
        self.error='有错误触发，请查看日志\n'
    def signFail(self):
        self.sign_fail='有人签到失败,请查看日志'
    def returnError(self):
        return self.error+self.sign_fail
error_fail=error_log()

def getAccount_num():
    try:
        with open('lists.json', 'r') as conf:
            lists = json.load(conf)
        return len(lists)
    except Exception as error:
        return '计数君错误: {}'.format(error)


Introduce = '回复“账号#密码”订阅自动打卡。\n' \
            '回复“del#账号”取消订阅打卡。\n' \
            '回复“安全承诺”获取安全支持。\n' \
            '注意事项:\n' \
            '多次密码错误会导致出现验证码服务而导致提示密码错误。\n'\
            '系统每日8点进行自动打卡，但不排除由于BUG或学校封IP导致打卡失败(目前未出现)。'
HAHA = '    打卡系统凝结了科技和二十位工作者的汗水。首先，我们通过手机定位获得您的经纬度坐标，采用超金坷垃遥感卫星测量您的晨间体温，再通过时空穿梭机结合遥感卫星获取您的午间体温。' \
       '最后，我们雇佣了二十位键盘侠在早上为您迅速填报。（滑稽）'

safe_ntro='     首先，本公众号由校内同学开发，目的在于分享学习，便捷他人；其次，本系统采用“用户——微信服务器——个人服务器——学校服务器”四点服务，微信服务器安全性绝对高；个人服务器位于腾讯云服务，因此其本身安全性没任何问题；' \
          '您发送的消息通过微信服务器转存入个人服务器，期间均采用AES加密，泄露可能性极低；个人服务器对接学校服务器相当于你登录信息门户，其中也是AES加密。\n' \
          '\n' \
          '综上所述，希望您放心使用，如需了解详情可在文章下留言。'