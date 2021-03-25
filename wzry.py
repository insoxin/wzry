# -*- coding: utf8 -*-
import re, requests, time
from random import randint
 
 
# 处理账号参数 浏览点赞任务
idlist = []
dict0 = {
    'gameOpenId': '',
    'gameRoleId': '',
    'gameServerId': '',
    'token': '',
    'userId': ''
}
 
dict1 = {
    'gameOpenId': '',
    'gameRoleId': '',
    'gameServerId': '',
    'token': '',
    'userId': ''
}
 
idlist.append(dict0)
idlist.append(dict1)
 
# 领取奖励参数
idlist1 = []
 
dict2 = {
    'serverId': '',
    'roleId': '',
    'userId': '',
    'gameOpenid': '',
    'openid': '',
    'msdkToken': '',
    'appOpenid': '',
    'timestamp': '',
    'sig': '',
    'msdkEncodeParam': ''
}
 
dict3 = {
    'serverId': '',
    'roleId': '',
    'userId': '',
    'gameOpenid': '',
    'openid': '',
    'msdkToken': '',
    'appOpenid': '',
    'timestamp': '',
    'sig': '',
    'msdkEncodeParam': ''
}
 
idlist1.append(dict2)
idlist1.append(dict3)
 
 
# 请求str转dict
def strtodict(str):
    str = re.sub(r'&', '\n', str)
    content = re.findall(r'(.*?)=(.*)', str)
    data = {}
    for i in content:
        key = i[0]
        value = i[1]
        data[key] = value
    return data
 
 
# 获取首页资讯
def get_zixun(dict):
    url = 'https://ssl.kohsocialapp.qq.com:10001/info/listinfo'
    data_str = os.environ["WZRY_h5sign"]
    data = strtodict(data_str)
    data.update(dict)
    data['rRand'] = str(int(time.time() * 1000))
    r = requests.post(url, data=data)
    for i in range(2, 8):
        try:
            # print(r.text)
            iInfoId = r.json()['data']['list'][i]['iInfoId']
            algoType = r.json()['data']['list'][i]['algoType']
            docid = r.json()['data']['list'][i]['docid']
            print(iInfoId, algoType)
            get_liulan(dict, i, iInfoId, algoType)
            time.sleep(randint(1, 3))
            get_dianzan(dict, docid, iInfoId)
        except:
            msg = f'第{str(i)}次获取文章参数失败'
            print(msg)
            return msg
    msg = '任务完成'
    return msg
 
    # print(data)
 
 
# 浏览资讯
def get_liulan(dict, pos, iInfoId, algoType):
    url = 'https://ssl.kohsocialapp.qq.com:10001/game/detailinfov3'
    data_str = os.environ["WZRY_h5sign"]
    data = strtodict(data_str)
    data.update(dict)
    data['rRand'] = str(int(time.time() * 1000))
    data['pos'] = pos
    data['iInfoId'] = iInfoId
    data['algoType'] = algoType
 
    requests.post(url, data=data)
 
 
# 点赞
def get_dianzan(dict, docid, iInfoId):
    url = 'https://ssl.kohsocialapp.qq.com:10001/user/addlike'
    data_str = os.environ["WZRY_h5sign"]
    data = strtodict(data_str)
    data.update(dict)
    data['rRand'] = str(int(time.time() * 1000))
    data['docid'] = docid
    data['iInfoId'] = iInfoId
    # print(data)
    r = requests.post(url, data=data)
    # print(r.text)
    if r.json()['data']['like'] == True:
        print('点赞成功')
 
 
# 领取浏览奖励
def get_liulan_lq(dict):
    url = 'https://ssl.kohsocialapp.qq.com:10001/play/h5taskgetgift'
    data_str = os.environ["WZRY_h5sign"]
    data = strtodict(data_str)
    data.update(dict)
    # data['timestamp'] = str(int(time.time() * 1000))
    data['taskId'] = '2019071900007'
    r = requests.post(url, data=data)
    # print(r.text)
    try:
        if r.json()['result'] == 0:
            msg = '浏览奖励领取成功'
        else:
            msg = r.json()['returnMsg']
    except:
        msg = '请求失败,请检查接口'
    return msg
 
 
# 领取点赞奖励
def get_dianzan_lq(dict):
    url = 'https://ssl.kohsocialapp.qq.com:10001/play/h5taskgetgift'
    data_str = os.environ["WZRY_h5sign"]
    data = strtodict(data_str)
    data.update(dict)
    # data['timestamp'] = str(int(time.time() * 1000))
    data['taskId'] = '2019071900008'
    r = requests.post(url, data=data)
    # print(r.text)
    try:
        if r.json()['result'] == 0:
            msg = '点赞奖励领取成功'
        else:
            msg = r.json()['returnMsg']
    except:
        msg = '请求失败,请检查接口'
    return msg
 
 
# 签到
def qiandao(dict):
    url = 'https://ssl.kohsocialapp.qq.com:10001/play/h5sign'
    data_str = os.environ["WZRY_h5sign"]
    data = strtodict(data_str)
    data.update(dict)
    # data['timestamp'] = str(int(time.time() * 1000))
    r = requests.post(url, data=data)
 
    try:
        if r.json()['result'] == 0:
            msg = '签到成功'
        else:
            msg = r.json()['returnMsg']
    except:
        msg = '请求失败,请检查接口'
    # print(data['serverId']+ ':  '+msg)
    return msg
 
 
def main_handler(event, context):
    n = 1
    msg = ''
    today = int(time.strftime("%w"))
    if today == 2:
        for i in idlist:
            get_zixun(i)
            msg_r = f'{str(n)}号，任务完成'
            msg = msg + msg_r + '\n'
            n += 1
        time.sleep(randint(2, 5))
 
    for i in idlist1:
        if today == 2:
            msg_r = get_dianzan_lq(i)
            msg = msg + msg_r + '\t'
            time.sleep(randint(1, 3))
 
            msg_r = get_liulan_lq(i)
            msg = msg + msg_r + '\t'
            time.sleep(randint(1, 3))
 
        msg_r = qiandao(i)
        msg = msg + msg_r + '\n'
 
    return msg
