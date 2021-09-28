#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 监控
# Desc      : 监控启动模块

import wbmonitor
import requests, json
#import urllib.parse
import logging
import time
import re

# 配置区
keywords = {"婴", "儿童", "尿"}

corpid = 'wwb83672685478bbbe'
AgentId = '1000002'
corpsecret = 'Frah3vmHcAaSbGWdPYJOgmVALwgNAzWYvx7KbqI7YkM'
# AgentId = '1000003'
# corpsecret = 'GVO52NYeeQdgrSpd2Wikje1QNyBRoZzZyexY9k5dFqQ'
# AgentId = '1000004'
# corpsecret = 'svupCDwX54V1NtuekwuOg58yW5khHyCnzrTLJy8Vpos'

#telegram机器人
tg_bot_token = "2023326569:AAHLs6ulU2-NnYXJRnHgx-9_I74AplihwwA"
tg_user_id = "-520508478"

#logfile_path = '/root/weibo/new.log'
logfile_path = 'new.log'

logging.basicConfig(level=logging.INFO, #控制台打印的日志级别
                    filename=logfile_path,
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s : %(message)s'
                    #'%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
##企业微信推送
# def qywx(msg):
#     server_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
#     re = requests.post(server_url)
#     jsontxt = json.loads(re.text)
#     access_token = jsontxt['access_token']
#     html = msg.replace('\n', '<br>')
#     url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
#     data = \
#         {
#             "touser": "@all",
#             "msgtype": "text",
#             #"agentid": "1000002",
#             "agentid": AgentId,
#             "text": {
#                 "content": html
#             },
#             "safe": 0
#         }
#     send_msges = (bytes(json.dumps(data), 'utf-8'))
#     res = requests.post(url, send_msges)
#     respon = res.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
#     print(respon)
#     print(res.text)
#     if respon['errmsg'] == "ok":
#         print(f"推送成功\n")
#     else:
#         print(f" 推送失败:鬼知道哪错了\n")
#     print("end")
	
##telegram推送
# def telegram_bot(title, content):
#     print("\n")
#     tg_bot_token = TG_BOT_TOKEN
#     tg_user_id = TG_USER_ID
#     if "TG_BOT_TOKEN" in os.environ and "TG_USER_ID" in os.environ:
#         tg_bot_token = os.environ["TG_BOT_TOKEN"]
#         tg_user_id = os.environ["TG_USER_ID"]
#     if not tg_bot_token or not tg_user_id:
#         print("Telegram推送的tg_bot_token或者tg_user_id未设置!!\n取消推送")
#         return
#     print("Telegram 推送开始")
#     send_data = {"chat_id": tg_user_id, "text": title +
#                                                 '\n\n' + content, "disable_web_page_preview": "true"}
#     response = requests.post(
#         url='https://api.telegram.org/bot%s/sendMessage' % (tg_bot_token), data=send_data)
#     print(response.text)
#
#
# now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# headers = {
#     'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; MI 6 MIUI/20.6.18)'
# }

def telegram_bot(title, content):
    print("\n")
    if not tg_bot_token or not tg_user_id:
        print("Telegram推送的tg_bot_token或者tg_user_id未设置!!\n取消推送")
        return
    print("Telegram 推送开始")
    url1 = 'https://api.telegram.org/bot%s/sendMessage' % (tg_bot_token)
    send_data = {"chat_id": tg_user_id, "text": title +
                                                '\n' + content, "disable_web_page_preview": "true"}
    response = requests.post(
        url='https://api.telegram.org/bot%s/sendMessage' % (tg_bot_token), data=send_data)
    print(response.text)

def keyword_compare(dicts):
    #print(dicts['text'])
    for i in keywords:
        if(i in dicts['text']):
            return 0
    return 1


def wbweixin(dicts):
    context = dicts['text'].replace('<br />', '\r')
    pattern = re.compile(r'<[^>]+>', re.S)
    result = pattern.sub('', context)
    text = "发送内容: "  + result + "\r"
    text += "发送时间: " + dicts['created_at'][0:20]+"\r"
    text += "宁关注的：" + dicts['nickName']+"发布微博啦\r"
    flag = qywx(text)
    return flag

def handlemessage(dicts):
    context = dicts['text'].replace('<br />', '\r')
    pattern = re.compile(r'<[^>]+>', re.S)
    result = pattern.sub('', context)
    text = "发送内容: "  + result + "\n"
    text += "发送时间: " + dicts['created_at'][0:20]+"\n"
    text += "宁关注的：" + dicts['nickName']+"发布微博啦\n"
    return text

def main():
    #微博部分
    w = wbmonitor.weiboMonitor()
    w.getweiboInfo()
    print("1")
    with open(wbmonitor.COMPARE_FILE,'r') as f:
        text = f.read()
        if text == '':
            w.getWBQueue()
    print("2")
    newWB = w.startmonitor()
    if newWB is not None:
        flag = keyword_compare(newWB)
        print("3")
        if(flag == 1):
            print("4")
            texts = handlemessage(newWB)
            telegram_bot("微博更新", texts)
            #print(wbweixin(newWB))  # 推送成功则输出True
        else:
            print("5")
            print("没有关键词")
    else:
        print("6")
        #print("没有更新内容")
        logging.info('没有更新')


if __name__ == '__main__':
    while(1):
        main()
        time.sleep(30)
