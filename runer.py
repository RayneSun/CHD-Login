# -*- coding:utf-8 -*-
import json
import time
import traceback
from lxml import etree
from random import randint
from login import login
import admin
import requests


doAction_url = 'http://service.chd.edu.cn/infoplus/interface/doAction'
start_url = 'http://service.chd.edu.cn/infoplus/form/XSYQSB/start'
table_url_start = 'http://service.chd.edu.cn/infoplus/interface/start'


def get_Table_url(location, cookie):
    sess = requests.Session()

    # 三个返回操作到http://service.chd.edu.cn/infoplus/form/XSYQSB/start
    sess.headers.update({
        'Connection': 'keep-alive',
        'Referer': 'http://ids.chd.edu.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
    })
    sess.cookies.update(cookie)
    try:
        start_page = sess.get(url=location)
        csrfToken = etree.HTML(start_page.text).xpath('//*[@itemscope="csrfToken"]/@content')[0]
    except:
        return None, None, None
    req_table_data = {
        'idc': 'XSYQSB',
        'release': '',
        'csrfToken': csrfToken,
        'formData': '{"_VAR_URL": "http://service.chd.edu.cn/infoplus/form/XSYQSB/start", "_VAR_URL_Attr": "{}"}'
    }
    # 申请表单
    table_page = sess.post(url=table_url_start, data=req_table_data)
    table_url = json.loads(table_page.text)["entities"][0]
    return table_url, csrfToken, sess


def signOne(account, password):
    # 签到获得重要cookie
    location, cookie = login(account=account, pwd=password)
    #密码错误？验证码？
    if location is None:
        return account + ': ' + cookie  # 此时cookie不是cookie而是错误信息

    # 获得表单，有时候会出错?
    table_url, csrfToken, sess = get_Table_url(cookie=cookie, location=location)

    _ = 3
    while table_url is None:
        _ -= 1
        time.sleep(0.5)  # 照顾一下服务器
        cookie, location = login(account=account, pwd=password)
        table_url, csrfToken, sess = get_Table_url(cookie=cookie, location=location)
        if _ == 0:
            break

    stepID = table_url.split('/')[-2]
    sess.headers.update({
        'Referer': 'http://service.chd.edu.cn/infoplus/form/{}/render'.format(stepID),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    })
    # 获得表单自动填写信息
    temp_data = {
        'stepId': stepID,
        'instanceId': '',
        'admin': 'false',
        'rand': '16.65865401406602',
        'width': '988',
        'lang': 'zh',
        'csrfToken': csrfToken
    }
    hist_data = sess.post(url='http://service.chd.edu.cn/infoplus/interface/render', data=temp_data).text
    hist_data = json.loads(hist_data)["entities"][0]["data"]
    form_data = {"_VAR_EXECUTE_INDEP_ORGANIZE_Name": "#", "_VAR_ACTION_INDEP_ORGANIZES_Codes": "2200",
                 "_VAR_ACTION_REALNAME": "#", "_VAR_ACTION_ORGANIZE": "2200", "_VAR_EXECUTE_ORGANIZE": "2200",
                 "_VAR_ACTION_INDEP_ORGANIZE": "2200", "_VAR_ACTION_INDEP_ORGANIZE_Name": "#",
                 "_VAR_ACTION_ORGANIZE_Name": "#", "_VAR_EXECUTE_ORGANIZES_Names": "#",
                 "_VAR_OWNER_ORGANIZES_Codes": "2200", "_VAR_ADDR": "202.117.71.27",
                 "_VAR_OWNER_ORGANIZES_Names": "#",
                 "_VAR_URL": "http://service.chd.edu.cn/infoplus/form/{}/render".format(stepID),
                 "_VAR_EXECUTE_ORGANIZE_Name": "#",
                 "_VAR_RELEASE": "true", "_VAR_NOW_MONTH": "11", "_VAR_ACTION_ACCOUNT": "#",
                 "_VAR_ACTION_INDEP_ORGANIZES_Names": "#", "_VAR_OWNER_ACCOUNT": "#",
                 "_VAR_ACTION_ORGANIZES_Names": "#", "_VAR_STEP_CODE": "xstx",
                 "_VAR_EXECUTE_ORGANIZES_Codes": "2200",
                 "_VAR_NOW_DAY": "7", "_VAR_OWNER_REALNAME": "#", "_VAR_NOW": "1604742313", "_VAR_URL_Attr": "{}",
                 "_VAR_ENTRY_NUMBER": "3491695", "_VAR_EXECUTE_INDEP_ORGANIZES_Names": "#",
                 "_VAR_STEP_NUMBER": stepID,
                 "_VAR_POSITIONS": "2200:3", "_VAR_EXECUTE_INDEP_ORGANIZES_Codes": "2200",
                 "_VAR_EXECUTE_POSITIONS": "2200:3", "_VAR_ACTION_ORGANIZES_Codes": "2200",
                 "_VAR_EXECUTE_INDEP_ORGANIZE": "2200", "_VAR_NOW_YEAR": "2020", "fieldTBR": "#",
                 "fieldTBR_Name": "#", "fieldSBSJ": 1604742313, "fieldGH": "#", "fieldBM": "2200",
                 "fieldBM_Name": "#", "fieldBJ": "", "fieldXB": "男", "fieldFDY": "#", "fieldJGSHENG": "#",
                 "fieldJGSHENG_Name": "#", "fieldJGSHI": "#", "fieldJGSHI_Name": "#",
                 "fieldJGSHI_Attr": "{\"_parent\":\"\"}", "fieldJGQU": "#", "fieldJGQU_Name": "#",
                 "fieldJGQU_Attr": "{\"_parent\":\"\"}", "fieldXXXS": "全日制", "fieldLQLB": "非定向就业",
                 "fieldSS": "#", "fieldLXFS": "13279317314", "fieldSFHBJ": "2", "fieldSFWH": "2",
                 "fieldZXQK": "1", "fieldXNSZQY": "#", "fieldXNSZQY_Name": "#", "fieldSZQY": "",
                 "fieldSZQY_Name": "", "fieldGW": "", "fieldSHENG": "陕西省", "fieldSHENG_Name": "陕西省", "fieldSHI": "西安市",
                 "fieldSHI_Name": "西安市", "fieldSHI_Attr": "{\"_parent\":\"陕西省\"}", "fieldQU": "碑林区",
                 "fieldQU_Name": "碑林区",
                 "fieldQU_Attr": "{\"_parent\":\"西安市\"}", "fieldZSDZ": "校内", "fieldYQFXDJ": "低风险地区",
                 "fieldYQFXDJ_Name": "低风险地区", "fieldGTJZRS": "0", "fieldQZRS": "0", "fieldYSRS": "0", "fieldJRTW": "15",
                 "fieldJRTW_Name": '', "fieldWJTW": "5", "fieldWJTW_Name": '', "fieldSFYS": "2",
                 "fieldYSQKSM": "",
                 "fieldSFQZHZ": "2", "fieldQZQKSM": "", "fieldSFJSGL": "2", "fieldGLLX": "", "fieldGLSJ": "",
                 "fieldGLDD": "", "fieldGLQKSM": "", "fieldSFKS": "2", "fieldZZMS": "", "fieldSF": "2",
                 "fieldJCHBXQ": "",
                 "fieldYHBJCSJ": "", "fieldSFJCWHRY": "2", "fieldJCWHXQ": "", "fieldYWHJCSJ": "", "fieldSFJCHZ": "2",
                 "fieldJCHZXQ": "", "fieldJCHZSJ": "", "fieldJTGJ": "", "fieldJTGJ_Name": "", "fieldCFSJ": "",
                 "fieldYJFXSJ": "", "fieldZD": "", "fieldZD_Name": "", "fieldHSRQ": "", "fieldHBCC": "",
                 "fieldSFQK": "2",
                 "fieldFKSJ": "", "fieldQKXQ": "", "fieldBZ": "", "fieldFJ": "", "fieldXLLX": "研究生", "fieldSFMD": "否",
                 "fieldFDYGH": "140021", "_VAR_ENTRY_NAME": "学生疫情上报__", "_VAR_ENTRY_TAGS": "研工部"}

    # 信息补全
    form_data.update(hist_data)
    randm, randa = randint(0, 10), randint(0, 10)
    form_data.update(
        {"fieldJRTW_Name": str(35.5 + randm * 0.1), "fieldJRTW": str(randm), "fieldWJTW_Name": str(35.5 + randa * 0.1),
         "fieldWJTW": str(randa), "fieldSFQK": "2"})

    # 上传签到结果
    doAction_data = {
        'actionId': '1',
        'formData': json.dumps(form_data),
        'remark': '',
        'nextUsers': '{}',
        'stepId': stepID,
        'timestamp': int(time.time()),
        'boundFields': 'fieldSFHBJ,fieldFDY,fieldSFJCWHRY,fieldSFQZHZ,fieldSBSJ,fieldYJFXSJ,fieldZZMS,fieldZD,fieldXLLX,fieldSFJCHZ,fieldFJ,fieldCFSJ,fieldGLSJ,fieldSFKS,fieldXXXS,fieldJRTW,fieldSZQY,fieldYHBJCSJ,fieldFDYGH,fieldSHENG,fieldFKSJ,fieldQU,fieldLXFS,fieldSFWH,fieldHBCC,fieldJGSHENG,fieldZXQK,fieldYSRS,fieldGW,fieldJTGJ,fieldQZRS,fieldGLLX,fieldYQFXDJ,fieldTBR,fieldYSQKSM,fieldSFMD,fieldXB,fieldSFQK,fieldSFYS,fieldLQLB,fieldJGSHI,fieldJCHZSJ,fieldJCHBXQ,fieldZSDZ,fieldHSRQ,fieldSF,fieldBJ,fieldQZQKSM,fieldQKXQ,fieldBM,fieldGTJZRS,fieldSS,fieldGH,fieldJCWHXQ,fieldXNSZQY,fieldSFJSGL,fieldBZ,fieldGLQKSM,fieldSHI,fieldWJTW,fieldJCHZXQ,fieldGLDD,fieldYWHJCSJ,fieldJGQU',
        'csrfToken': csrfToken,
        'lang': 'zh'
    }
    mess = sess.post(url=doAction_url, data=doAction_data).text

    # 签到完成
    if json.loads(mess)['ecode'] == "SUCCEED":
        return account + ': 签到成功'
    else:
        return account + ': 失败响应: ' + mess


def main():
    try:
        with open('lists.json', 'r') as conf:
            lists = json.load(conf)

        print(time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime()))
        print("共计签到{}人".format(len(lists)))

        for account, password in lists.items():
            mess = signOne(account=account, password=password)
            print(mess)
            if mess[-4:] != '签到成功':
                admin.error_fail.signFail()
        time.sleep(1)  # 可怜一下服务器

    except:
        admin.error_fail.errorOccur()
        print('ERROR')
        print(traceback.format_exc())


main()
