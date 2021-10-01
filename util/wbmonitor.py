#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 微博
# Desc      : 微博主模块

import requests
import os
import util.yamlutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 这里导入被监控用户的uid
data_all = util.yamlutil.data_all
for yam_data in data_all:
    if 'uid' in yam_data:
        wbuid = yam_data['uid']
        break


class WeiboMonitor:
    def __init__(self, ):
        self.reqHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://passport.weibo.cn/signin/login',
            'Connection': 'close',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }
        self.comparefile = os.path.join(BASE_DIR, 'wbIds.txt')
        self.itemids = []
        self.weiboInfo = []
        self.uid = wbuid
    
    # 获取访问连接
    def getweiboinfo(self):
        try:
            self.weiboInfo = []
            for i in self.uid:
                userinfo = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=%s' % i
                res = requests.get(userinfo, headers=self.reqHeaders)
                for j in res.json()['data']['tabsInfo']['tabs']:
                    if j['tab_type'] == 'weibo':
                        self.weiboInfo.append('https://m.weibo.cn/api/container/'
                                              'getIndex?type=uid&value=%s&containerid=%s' % (i, j['containerid']))
        except Exception as e:
            self.echo_msg('Error', e)
            # sys.exit()        为了代码不异常退出，这里注释掉
    
    # 收集已经发布动态的id
    def getwb_queue(self):
        try:
            self.itemids = []
            for i in self.weiboInfo:
                res = requests.get(i, headers=self.reqHeaders)
                
                with open(self.comparefile, 'a') as f:
                    for j in res.json()['data']['cards']:
                        if j['card_type'] == 9:
                            f.write(j['mblog']['id'] + '\n')
                            self.itemids.append(j['mblog']['id'])
            self.echo_msg('Info', '微博数目获取成功')
            self.echo_msg('Info', '目前有 %s 条微博' % len(self.itemids))
        except Exception as e:
            self.echo_msg('Error', e)
            # sys.exit()        为了代码不异常退出，这里注释掉
    
    # 开始监控
    def startmonitor(self, ):
        returndict = {}  # 获取微博相关内容，编辑为邮件
        try:
            itemids = []
            with open(self.comparefile, 'r') as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    itemids.append(line)
            for i in self.weiboInfo:
                res = requests.get(i, headers=self.reqHeaders)
                for j in res.json()['data']['cards']:
                    if j['card_type'] == 9:
                        if str(j['mblog']['id']) not in itemids:
                            with open(self.comparefile, 'a') as f:
                                f.write(j['mblog']['id'] + '\n')
                            self.echo_msg('Info', '发微博啦!!!')
                            self.echo_msg('Info', '目前有 %s 条微博' % (len(itemids) + 1))
                            returndict['created_at'] = j['mblog']['created_at']
                            returndict['text'] = j['mblog']['text']
                            returndict['source'] = j['mblog']['source']
                            returndict['nickName'] = j['mblog']['user']['screen_name']
                            return returndict
        except Exception as e:
            self.echo_msg('Error', e)
            # sys.exit()        为了代码不异常退出，这里注释掉
    
    # 格式化输出
    @staticmethod
    def echo_msg(level, msg):
        if level == 'Info':
            print('[Info] %s' % msg)
        elif level == 'Error':
            print('[Error] %s' % msg)
            