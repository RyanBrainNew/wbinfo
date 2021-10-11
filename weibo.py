#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 监控
# Desc      : 监控启动模块

import util.wbmonitor
import util.push
import util.yamlutil
import logging
import time
import os
import datetime


# 输出到日志文件
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename=os.path.join(BASE_DIR, 'new.log'),
                    filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s : %(message)s'
                    # '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )

# 关键词过滤
data_all = util.yamlutil.data_all
for yam_data in data_all:
    if 'keywords' in yam_data:
        keywords = yam_data['keywords']
        break


def keyword_compare(dicts):
    # print(dicts['text'])
    for i in keywords:
        if i in dicts['text']:
            return 0
    return 1


def main():
    # 添加勿扰模式，固定时间段不推送
    # nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    now_time = datetime.datetime.now()
    now_hour = now_time.strftime('%H')
    # now_minute = now_time.strftime('%M')
    
    # 微博部分
    w = util.wbmonitor.WeiboMonitor()
    w.getweiboinfo()
    with open(w.comparefile, 'r') as f:
        text = f.read()
        if text == '':
            w.getwb_queue()
    new_wb = w.startmonitor()
    if new_wb is not None:
        keyword_notexist_flag = keyword_compare(new_wb)
        if keyword_notexist_flag == 1:
            logging.info('准备推送')
            # 设置勿扰时段，收集到新微博id，但是不推送
            if '01' <= now_hour <= '07':
                logging.info('勿扰时间段不推送')
                print('勿扰时间段不推送')
                return
            # if 1:
            #     texts = util.push.PushChannels.telegram_handlemessage(new_wb)
            #     util.push.PushChannels.telegram_push(texts)  # 用telegram机器人推送
            if 1:
                texts = util.push.PushChannels.wechat_handlemessage(new_wb)
                util.push.PushChannels.wechat_push(texts)  # 用企业微信推送

        else:
            print("没有关键词")
    else:
        # print("没有更新内容")
        logging.info('没有更新')


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(30)
