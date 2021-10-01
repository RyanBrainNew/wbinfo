#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 微博
# Desc      : 微博主模块
import requests
import json
import re
import util.yamlutil

# 从配置文件中获取telegram、WeChat的推送参数，避免隐私信息明文写在代码里
data_all = util.yamlutil.data_all
for yam_data in data_all:
    if 'TelegramConfig' in yam_data:
        tg_bot_token = yam_data['TelegramConfig']['tg_bot_token']
        tg_user_id = yam_data['TelegramConfig']['tg_user_id']
    elif 'WechatConfig' in yam_data:
        corpid = yam_data['WechatConfig']['corpid']
        agentid = yam_data['WechatConfig']['agentid']
        corpsecret = yam_data['WechatConfig']['corpsecret']


class PushChannels:
    # 初始化方法，判断文件是否存在
    def __init__(self):
        self._content = "test"  # 默认没有读取过文件

    # 电报机器人推送,由于没用到self，需要设置静态函数
    @staticmethod
    def telegram_push(content):
        if not tg_bot_token or not tg_user_id:
            print("Telegram推送的tg_bot_token或者tg_user_id未设置!!\n取消推送")
            return
        send_data = {"chat_id": tg_user_id, "text": '\n' + str(content), "disable_web_page_preview": "true"}
        response = requests.post(url='https://api.telegram.org/bot%s/sendMessage' % tg_bot_token,
                                 data=send_data, timeout=5)
        if response.status_code != 200:
            print(f"访问失败\n")
            return
        respon = response.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        if respon['ok']:
            print(f"推送成功\n")
        else:
            print(f"推送失败:鬼知道哪错了\n")

    # 处理电报推送的文本,去除html格式    形参后面加入:type 可以限定传入形参的类型,由于没用到self，需要设置静态函数
    @staticmethod
    def telegram_handlemessage(dicts: dict):
        context = dicts['text'].replace('<br />', '\r')
        pattern = re.compile(r'<[^>]+>', re.S)
        result = pattern.sub('', context)
        text = "发送内容: " + result + "\n"
        text += "发送时间: " + dicts['created_at'][0:20]+"\n"
        text += "宁关注的：" + dicts['nickName']+"发布微博啦\n"
        return text

    # 企业微信推送,由于没用到self，需要设置静态函数
    @staticmethod
    def wechat_push(msg):
        server_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
        response = requests.post(server_url)
        jsontxt = json.loads(response.text)
        access_token = jsontxt['access_token']
        html = str(msg).replace('\n', '<br>')
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        data = \
            {
                "touser": "@all",
                "msgtype": "text",
                "agentid": agentid,
                "text": {
                    "content": html
                },
                "safe": 0
            }
        send_msges = (bytes(json.dumps(data), 'utf-8'))
        res = requests.post(url, send_msges, timeout=5)
        respon = res.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        if respon['errmsg'] == "ok":
            print(f"推送成功\n")
        else:
            print(f" 推送失败:鬼知道哪错了\n")

    # 处理微信推送的文本,去除html格式,由于没用到self，需要设置静态函数
    @staticmethod
    def wechat_handlemessage(dicts: dict):
        context = dicts['text'].replace('<br />', '\r')
        pattern = re.compile(r'<[^>]+>', re.S)
        result = pattern.sub('', context)
        text = "发送内容: " + result + "\r"
        text += "发送时间: " + dicts['created_at'][0:20]+"\r"
        text += "宁关注的：" + dicts['nickName']+"发布微博啦\r"
        return text
