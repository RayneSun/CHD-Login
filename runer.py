# -*- coding:utf-8 -*-
import requests
import json
from lxml import etree
from login import loginIn
from random import random
import os

doAction_url = 'http://service.chd.edu.cn/infoplus/interface/doAction'


def get_Table_url(cookie, location):
    start_url = 'http://service.chd.edu.cn/infoplus/form/XSYQSB/start'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Cookie': cookie,
        'Host': 'service.chd.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://ids.chd.edu.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
    }

    # 两个返回操作
    temp = requests.get(url=location, headers=headers, allow_redirects=False).headers
    while temp.get('Location') is None:
        print('Ops')
        return None, None
    _ = requests.get(url=temp['Location'], headers=headers, allow_redirects=False).headers

    # 获得csrfToken
    start_page = requests.get(url=start_url, headers=headers)
    csrfToken = etree.HTML(start_page.content.decode('utf-8')).xpath('//*[@itemscope="csrfToken"]/@content')[0]

    req_table_data = {
        'idc': 'XSYQSB',
        'release': '',
        'csrfToken': csrfToken,
        'formData': '{"_VAR_URL": "http://service.chd.edu.cn/infoplus/form/XSYQSB/start", "_VAR_URL_Attr": "{}"}'
    }
    req_table_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Length': '204',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Host': 'service.chd.edu.cn',
        'Origin': 'http://service.chd.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://service.chd.edu.cn/infoplus/form/XSYQSB/start',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63',

    }
    table_url_start = 'http://service.chd.edu.cn/infoplus/interface/start'

    # 包含表单的内容
    table_page = requests.post(url=table_url_start, headers=req_table_headers, data=req_table_data)
    table_url = json.loads(table_page.text)["entities"][0]
    return table_url, csrfToken


def signOne(account, password):
    cookie, location = loginIn(account=account, password=password)

    if cookie is None:  # 密码错误
        return False, account
    table_url, csrfToken = get_Table_url(cookie=cookie, location=location)

    while table_url is None:
        cookie, location = loginIn(account=account, password=password)

        if cookie is None:  # 密码错误
            return False, account
        table_url, csrfToken = get_Table_url(cookie=cookie, location=location)

    stepID = table_url.split('/')[-2]

    doAction_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
        'Host': 'service.chd.edu.cn',
        'Origin': 'http://service.chd.edu.cn',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://service.chd.edu.cn/infoplus/form/{}/render'.format(stepID),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 获得表单自动填写信息
    data = {
        'stepId': stepID,
        'instanceId': '',
        'admin': 'false',
        'rand': '16.65865401406602',
        'width': '988',
        'lang': 'zh',
        'csrfToken': csrfToken
    }
    hist_info = requests.post(url='http://service.chd.edu.cn/infoplus/interface/render', headers=doAction_headers,
                              data=data).text
    hist_info = json.loads(hist_info)["entities"][0]["data"]

    # 信息补全
    randm, randa = float(format(random(), '.1f')), float(format(random(), '.1f'))
    formData = {"_VAR_EXECUTE_INDEP_ORGANIZE_Name": "汽车学院", "_VAR_ACTION_INDEP_ORGANIZES_Codes": "2200",
                "_VAR_ACTION_REALNAME": "李旭川", "_VAR_ACTION_ORGANIZE": "2200", "_VAR_EXECUTE_ORGANIZE": "2200",
                "_VAR_ACTION_INDEP_ORGANIZE": "2200", "_VAR_ACTION_INDEP_ORGANIZE_Name": "汽车学院",
                "_VAR_ACTION_ORGANIZE_Name": "汽车学院", "_VAR_EXECUTE_ORGANIZES_Names": "汽车学院",
                "_VAR_OWNER_ORGANIZES_Codes": "2200", "_VAR_ADDR": "202.117.71.27",
                "_VAR_OWNER_ORGANIZES_Names": "汽车学院",
                "_VAR_URL": "http://service.chd.edu.cn/infoplus/form/{}/render".format(stepID),
                "_VAR_EXECUTE_ORGANIZE_Name": "汽车学院",
                "_VAR_RELEASE": "true", "_VAR_NOW_MONTH": "11", "_VAR_ACTION_ACCOUNT": "2018222064",
                "_VAR_ACTION_INDEP_ORGANIZES_Names": "汽车学院", "_VAR_OWNER_ACCOUNT": "2018222064",
                "_VAR_ACTION_ORGANIZES_Names": "汽车学院", "_VAR_STEP_CODE": "xstx", "_VAR_EXECUTE_ORGANIZES_Codes": "2200",
                "_VAR_NOW_DAY": "7", "_VAR_OWNER_REALNAME": "李旭川", "_VAR_NOW": "1604742313", "_VAR_URL_Attr": "{}",
                "_VAR_ENTRY_NUMBER": "3491695", "_VAR_EXECUTE_INDEP_ORGANIZES_Names": "汽车学院",
                "_VAR_STEP_NUMBER": stepID,
                "_VAR_POSITIONS": "2200:3", "_VAR_EXECUTE_INDEP_ORGANIZES_Codes": "2200",
                "_VAR_EXECUTE_POSITIONS": "2200:3", "_VAR_ACTION_ORGANIZES_Codes": "2200",
                "_VAR_EXECUTE_INDEP_ORGANIZE": "2200", "_VAR_NOW_YEAR": "2020", "fieldTBR": "2018222064",
                "fieldTBR_Name": "李旭川", "fieldSBSJ": 1604742313, "fieldGH": "2018222064", "fieldBM": "2200",
                "fieldBM_Name": "汽车学院", "fieldBJ": "", "fieldXB": "男", "fieldFDY": "郑文捷", "fieldJGSHENG": "宁夏回族自治区",
                "fieldJGSHENG_Name": "宁夏回族自治区", "fieldJGSHI": "吴忠市", "fieldJGSHI_Name": "吴忠市",
                "fieldJGSHI_Attr": "{\"_parent\":\"\"}", "fieldJGQU": "青铜峡市", "fieldJGQU_Name": "青铜峡市",
                "fieldJGQU_Attr": "{\"_parent\":\"\"}", "fieldXXXS": "全日制", "fieldLQLB": "非定向就业",
                "fieldSS": "校本部(北院)07号楼421", "fieldLXFS": "13279317314", "fieldSFHBJ": "2", "fieldSFWH": "2",
                "fieldZXQK": "1", "fieldXNSZQY": "南校区（校本部北院）", "fieldXNSZQY_Name": "南校区（校本部北院）", "fieldSZQY": "",
                "fieldSZQY_Name": "", "fieldGW": "", "fieldSHENG": "陕西省", "fieldSHENG_Name": "陕西省", "fieldSHI": "西安市",
                "fieldSHI_Name": "西安市", "fieldSHI_Attr": "{\"_parent\":\"陕西省\"}", "fieldQU": "碑林区",
                "fieldQU_Name": "碑林区",
                "fieldQU_Attr": "{\"_parent\":\"西安市\"}", "fieldZSDZ": "校内", "fieldYQFXDJ": "低风险地区",
                "fieldYQFXDJ_Name": "低风险地区", "fieldGTJZRS": "0", "fieldQZRS": "0", "fieldYSRS": "0", "fieldJRTW": "15",
                "fieldJRTW_Name": 36 + randm, "fieldWJTW": "15", "fieldWJTW_Name": 36 + randa, "fieldSFYS": "2",
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
    formData.update(hist_info)
    # print(formData)

    # 上传
    doAction_data = {
        'actionId': '1',
        'formData': json.dumps(formData),
        'remark': '',
        'nextUsers': '{}',
        'stepId': stepID,
        'timestamp': '1604740866',
        'boundFields': 'fieldSFHBJ,fieldFDY,fieldSFJCWHRY,fieldSFQZHZ,fieldSBSJ,fieldYJFXSJ,fieldZZMS,fieldZD,fieldXLLX,fieldSFJCHZ,fieldFJ,fieldCFSJ,fieldGLSJ,fieldSFKS,fieldXXXS,fieldJRTW,fieldSZQY,fieldYHBJCSJ,fieldFDYGH,fieldSHENG,fieldFKSJ,fieldQU,fieldLXFS,fieldSFWH,fieldHBCC,fieldJGSHENG,fieldZXQK,fieldYSRS,fieldGW,fieldJTGJ,fieldQZRS,fieldGLLX,fieldYQFXDJ,fieldTBR,fieldYSQKSM,fieldSFMD,fieldXB,fieldSFQK,fieldSFYS,fieldLQLB,fieldJGSHI,fieldJCHZSJ,fieldJCHBXQ,fieldZSDZ,fieldHSRQ,fieldSF,fieldBJ,fieldQZQKSM,fieldQKXQ,fieldBM,fieldGTJZRS,fieldSS,fieldGH,fieldJCWHXQ,fieldXNSZQY,fieldSFJSGL,fieldBZ,fieldGLQKSM,fieldSHI,fieldWJTW,fieldJCHZXQ,fieldGLDD,fieldYWHJCSJ,fieldJGQU',
        'csrfToken': csrfToken,
        'lang': 'zh'
    }
    mess = requests.post(url=doAction_url, headers=doAction_headers, data=doAction_data).text

    # 签到完成
    if json.loads(mess)['ecode'] == "SUCCEED":
        return True, hist_info['_VAR_ACTION_REALNAME']


def main():
    with open('lists.json', 'r') as conf:
        lists = json.load(conf)
    for account, password in lists.items():
        flag, mess = signOne(account=account, password=password)
        if flag:
            print(mess + " 今日已签到完成！")
        else:
            print(mess + " 密码错误！")
    os.system('pause')


main()
