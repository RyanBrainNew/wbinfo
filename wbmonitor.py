#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 微博
# Desc      : 微博主模块

import requests,json,sys
global COMPARE_FILE
#COMPARE_FILE = "/root/WeiBo/wbIds.txt"
COMPARE_FILE = "wbIds.txt"

class weiboMonitor():
	def __init__(self, ):
		self.reqHeaders = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Referer': 'https://passport.weibo.cn/signin/login',
			'Connection': 'close',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
		}
		# self.uid = ['1927305954','7347878145','2717718713']#这里添加关注人的uid
		self.uid = ['5069029750', '2048344461', '3977917853', '1779290792', '1862323381']  # 这里添加关注人的uid
		# 薅羊毛大队长 5069029750
		# 请与白菜同归于尽 2048344461
		# 不薅羊毛了 3977917853
		# 默默薅羊毛 1779290792
		# 东民上车了 1862323381
	#获取访问连接
	def getweiboInfo(self):
		try:
			self.weiboInfo = []
			for i in self.uid:
				userInfo = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s'%(i)
				res = requests.get(userInfo,headers=self.reqHeaders)
				for j in res.json()['data']['tabsInfo']['tabs']:
					if j['tab_type'] == 'weibo':
						self.weiboInfo.append('https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=%s'%(i,j['containerid']))
		except Exception as e:
			self.echoMsg('Error',e)
			sys.exit()
	#收集已经发布动态的id
	def getWBQueue(self):
		try:
			self.itemIds = []
			for i in self.weiboInfo:
				res = requests.get(i,headers=self.reqHeaders)

				with open(COMPARE_FILE, 'a') as f:
					for j in res.json()['data']['cards']:
						if j['card_type'] == 9:
							f.write(j['mblog']['id']+'\n')
							self.itemIds.append(j['mblog']['id'])
			self.echoMsg('Info','微博数目获取成功')
			self.echoMsg('Info','目前有 %s 条微博'%len(self.itemIds))
		except Exception as e:
			self.echoMsg('Error',e)
			sys.exit()
	#开始监控
	def startmonitor(self, ):
		returnDict = {} #获取微博相关内容，编辑为邮件
		try:
			itemIds = []
			with open(COMPARE_FILE,'r') as f:
				for line in f.readlines():
					line = line.strip('\n')
					itemIds.append(line)
			for i in self.weiboInfo:
				res = requests.get(i,headers=self.reqHeaders)
				for j in res.json()['data']['cards']:
					if j['card_type'] == 9:
						if str(j['mblog']['id']) not in itemIds:
							with open(COMPARE_FILE,'a') as f:
								f.write(j['mblog']['id']+'\n')
							self.echoMsg('Info','发微博啦!!!')
							self.echoMsg('Info','目前有 %s 条微博'%(len(itemIds)+1))
							returnDict['created_at'] = j['mblog']['created_at']
							returnDict['text'] = j['mblog']['text']
							returnDict['source'] = j['mblog']['source']
							returnDict['nickName'] = j['mblog']['user']['screen_name']
							return returnDict
		except Exception as e:
			self.echoMsg('Error',e)
			sys.exit()
	#格式化输出
	def echoMsg(self, level, msg):
		if level == 'Info':
			print('[Info] %s'%msg)
		elif level == 'Error':
			print('[Error] %s'%msg)
