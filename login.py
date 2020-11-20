# -*- coding:utf-8 -*-
import requests
import execjs
from lxml import etree
import time
import json
sign_init_url = 'http://service.chd.edu.cn/infoplus/form/XSYQSB/start'
login_url='http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fservice.chd.edu.cn%2Finfoplus%2Flogin%3FretUrl%3Dhttp%253A%252F%252Fservice.chd.edu.cn%252Finfoplus%252Fform%252FXSYQSB%252Fstart'


def login(account,pwd):
    sess=requests.Session()
    sess.headers.update({
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'.replace(' ','')
    })
    # 第一步，得到登录界面及cookie
    response=sess.get(url=sign_init_url,allow_redirects=False)
    redirect_url = 'http://service.chd.edu.cn' + response.headers.get('Location')
    needed_cookie=response.cookies.get_dict()
    #第二部，获得登陆界面要素
    response = etree.HTML(sess.get(url=redirect_url).text)
    # 登录二要素
    pwdEncryptSalt = response.xpath('//*[@id="pwdEncryptSalt"]/@value')[0]
    execution = response.xpath('//*[@id="execution"]/@value')[0]
    # 加密部分
    encrypt_js = sess.get('http://ids.chd.edu.cn/authserver/customTheme/static/common/encrypt.js').text
    encryptJS = execjs.compile(source=encrypt_js)
    encoded_pwd = encryptJS.call('encryptAES', pwd, pwdEncryptSalt)
    #验证码需求
    tim = time.time()
    tim = str(int(tim * 1000))
    captcha_url = 'http://ids.chd.edu.cn/authserver/checkNeedCaptcha.htl?username=' + account + '&_=' + tim
    if json.loads(sess.get(url=captcha_url).text).get("isNeed"):
        return None,'系统要求验证码识别，请在网页版进行一次登录再试'
    # 登录初始化
    post_data = {
        'username': account,
        'password': encoded_pwd,
        'captcha': '',
        '_eventId': 'submit',
        'cllt': 'userNameLogin',
        'lt': '',
        'execution': execution
    }
    #登录
    sess.headers.update({
        'Referer': 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fservice.chd.edu.cn%2Finfoplus%2Flogin%3FretUrl%3Dhttp%253A%252F%252Fservice.chd.edu.cn%252Finfoplus%252Fform%252FXSYQSB%252Fstart',
    })
    response = sess.post(url=login_url, data=post_data, allow_redirects=False)

    if response.status_code==302:
        return response.headers['Location'], needed_cookie
    else:
        return None,'密码错误！'