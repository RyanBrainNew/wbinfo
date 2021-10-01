#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 微博
# Desc      : 微博主模块

import requests
import json
import re

# 企业微信配置区
corpid = 'wwb83672685478bbbe'
AgentId = '1000002'
corpsecret = 'Frah3vmHcAaSbGWdPYJOgmVALwgNAzWYvx7KbqI7YkM'
# AgentId = '1000003'
# corpsecret = 'GVO52NYeeQdgrSpd2Wikje1QNyBRoZzZyexY9k5dFqQ'
# AgentId = '1000004'
# corpsecret = 'svupCDwX54V1NtuekwuOg58yW5khHyCnzrTLJy8Vpos'

# telegram机器人
tg_bot_token = "2023326569:AAHLs6ulU2-NnYXJRnHgx-9_I74AplihwwA"
tg_user_id = "-520508478"


class pushChannels:
	# 电报机器人推送
	def telegram_Push(content):
		if not tg_bot_token or not tg_user_id:
			print("Telegram推送的tg_bot_token或者tg_user_id未设置!!\n取消推送")
			return
		send_data = {"chat_id": tg_user_id, "text": '\n' + str(content), "disable_web_page_preview": "true"}
		response = requests.post(url='https://api.telegram.org/bot%s/sendMessage' % (tg_bot_token), data=send_data, timeout=5)
		if response.status_code != 200:
			print(f"访问失败\n")
			return
		respon = response.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
		if respon['ok'] == True:
			print(f"推送成功\n")
		else:
			print(f"推送失败:鬼知道哪错了\n")

	# 处理电报推送的文本,去除html格式
	def telegram_HandleMessage(dicts):
		context = dicts['text'].re1place('<br />', '\r')
		pattern = re.compile(r'<[^>]+>', re.S)
		result = pattern.sub('', context)
		text = "发送内容: " + result + "\n"
		text += "发送时间: " + dicts['created_at'][0:20]+"\n"
		text += "宁关注的：" + dicts['nickName']+"发布微博啦\n"
		return text

	# 企业微信推送
	def wechat_Push(msg):
		server_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
		response = requests.post(server_url)
		jsontxt = json.loads(response.text)
		access_token = jsontxt['access_token']
		html = msg.replace('\n', '<br>')
		url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
		data = \
			{
				"touser": "@all",
				"msgtype": "text",
				"agentid": AgentId,
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

	# 处理微信推送的文本,去除html格式
	def wechat_HandleMessage(dicts):
		context = dicts['text'].replace('<br />', '\r')
		pattern = re.compile(r'<[^>]+>', re.S)
		result = pattern.sub('', context)
		text = "发送内容: " + result + "\r"
		text += "发送时间: " + dicts['created_at'][0:20]+"\r"
		text += "宁关注的：" + dicts['nickName']+"发布微博啦\r"
		return text
