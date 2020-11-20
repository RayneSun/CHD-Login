from login import login
import json
import traceback
import admin

JSON_LISTS='lists.json'

def updater(strs='2018222064#Biglocker.1518'): #'2018222066#abcde'
    try:
        mess=strs.split('#')
        if len(mess) !=2:
            return "您发的格式有误"
        [key,value]=mess
        #删除订阅服务
        if key=='del':
            with open(JSON_LISTS, 'r') as conf:
                lists = json.load(conf)
            if lists.get(value) is None:
                return '您压根没订阅哟~'
            else:
                lists.pop(value)
                lists_to_json = json.dumps(lists)
                with open(JSON_LISTS, 'w') as conf:
                    conf.write(lists_to_json)
            return '删除成功了哟'
        else:#不是删除
            with open(JSON_LISTS, 'r') as conf:
                lists = json.load(conf)
            if lists.get(key) is not None:
                return "您重复操作了哟"
            else:#没重复操作
                location, cookie = login(account=key, pwd=value)
                if location is None:  # 密码错误或多次输错
                    return cookie
                else:
                    lists.update({key:value})
                    lists_to_json=json.dumps(lists)
                    with open(JSON_LISTS, 'w') as conf:
                        conf.write(lists_to_json)
                    return "订阅成功哟"
    except:
        traceback.print_exc()
        admin.error_fail.errorOccur()
        return "非常抱歉服务器出现BUG，开发者已收到消息"
