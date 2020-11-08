import requests
import execjs
import re
from lxml import etree



def init():
    sign_init_url = 'http://service.chd.edu.cn/infoplus/form/XSYQSB/start'
    sign_init_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': 'service.chd.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }

    # 第一步，得到登录界面及cookie
    sign_init_response_headers = requests.get(url=sign_init_url, headers=sign_init_headers,
                                              allow_redirects=False).headers

    login_url = 'http://service.chd.edu.cn' + sign_init_response_headers['Location']
    login_headers = sign_init_headers.copy()
    login_headers.update({'Cookie': sign_init_response_headers['Set-Cookie']})
    return login_url, login_headers


# 第二步，得到二级登陆页面
def loginIn(account, password):
    login_url, login_headers = init()
    login_url_2 = requests.get(url=login_url, headers=login_headers, allow_redirects=False).headers['Location']

    login_url_2_response = requests.get(url=login_url_2, headers=login_headers, allow_redirects=False)

    # 登录三要素
    before_login_headers = {
        'Accept': 'text/css,*/*;q=0.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': 'ids.chd.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    before_login_headers.update({'cookie': login_url_2_response.headers['Set-Cookie'].replace(',', ';')})
    before_login_headers.update({'Referer': login_url_2})

    pwdDefaultEncryptSalt = re.findall('pwdDefaultEncryptSalt = "(.*?)"', login_url_2_response.content.decode('utf-8'))[0]
    lt = etree.HTML(login_url_2_response.content.decode('utf-8')).xpath('//*[@name="lt"]/@value')[0]

    #加密密码
    encrypy_url = 'http://ids.chd.edu.cn/authserver/custom/js/encrypt.js'
    encrypy_js = requests.get(url=encrypy_url, headers=before_login_headers).text
    encrypy_js = execjs.compile(encrypy_js)
    encoded_password = encrypy_js.call('encryptAES', password, pwdDefaultEncryptSalt)

    #登录
    data = {
        'username': account,
        'password': encoded_password,
        'lt': lt,
        'dllt': 'userNamePasswordLogin',
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rmShown': '1'
    }
    temp = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Content-Length': '278',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ids.chd.edu.cn',
        'Origin': 'http://ids.chd.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': login_url_2,
        'Upgrade-Insecure-Requests': '1'

    }
    before_login_headers.update(temp)
    final = requests.post(url=login_url_2, headers=before_login_headers, data=data, allow_redirects=False)

    #获得登陆后cookie
    if final.headers.get('Set-Cookie') is None:
        return None, None
    cookie=final.headers['Set-Cookie']
    cookie = cookie.replace(',', ';').split(';')
    location = final.headers['Location']
    for str in cookie:
        if str[:20] == ' iPlanetDirectoryPro':
            return login_headers['Cookie'] + ';' + str, location


