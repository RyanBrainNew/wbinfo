#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 监控
# Desc      : 监控启动模块

import wbmonitor
import requests, json
import urllib.parse
import logging
import time
import re

corpid = 'wwb83672685478bbbe'
# AgentId = '1000002'
# corpsecret = 'Frah3vmHcAaSbGWdPYJOgmVALwgNAzWYvx7KbqI7YkM'
AgentId = '1000003'
corpsecret = 'GVO52NYeeQdgrSpd2Wikje1QNyBRoZzZyexY9k5dFqQ'

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    #filename='/root/WeiBo/new.log',
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s : %(message)s'
                    #'%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
##企业微信推送
def qywx(msg):
    server_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    re = requests.post(server_url)
    jsontxt = json.loads(re.text)
    access_token = jsontxt['access_token']
    html = msg.replace('\n', '<br>')
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
    data = \
        {
            "touser": "@all",
            "msgtype": "text",
            #"agentid": "1000002",
            "agentid": AgentId,
            "text": {
                "content": html
            },
            "safe": 0
        }
    send_msges = (bytes(json.dumps(data), 'utf-8'))
    res = requests.post(url, send_msges)
    respon = res.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
    print(respon)
    print(res.text)
    if respon['errmsg'] == "ok":
        print(f"推送成功\r")
    else:
        print(f" 推送失败:鬼知道哪错了\r")
    print("end")


#python去除html标签的几种方法
#https://www.cnblogs.com/zhangyafei/p/10285378.html

def wbweixin(dicts):
    text = "宁关注的："+dicts['nickName']+"发布微博啦\r"
    text += "发送时间: "+dicts['created_at'][0:20]+"\r"
    #text += "发送时间: " + dicts['text'] + "\r"
    #下面做简单的标签处理，在微信上可以正确显示格式
    context = dicts['text'].replace('<br />', '\r')
    pattern = re.compile(r'<[^>]+>', re.S)
    result = pattern.sub('', context)
    text += "发送内容: " + result
    #text += "发送内容: " + dicts['text']
    flag = qywx(text)
    return flag


def main():
    #微博部分
    w = wbmonitor.weiboMonitor()
    w.getweiboInfo()
    with open(wbmonitor.COMPARE_FILE,'r') as f:
        text = f.read()
        if text == '':
            w.getWBQueue()
    newWB = w.startmonitor()
    if newWB is not None:
        print(wbweixin(newWB))#推送成功则输出True
    else:
        #print("没有更新内容")
        logging.info('没有更新')


if __name__ == '__main__':
    while(1):
        main()
        time.sleep(5)
