#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : B1ain
# Action    : 监控
# Desc      : 监控启动模块

import wbmonitor
import push
import logging
import time

# 输出到日志文件
# logfile_path = '/root/weibo/new.log'
logfile_path = 'new.log'

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename=logfile_path,
                    filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s : %(message)s'
                    # '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


# 关键词过滤
keywords = {"婴", "儿童", "尿"}


def keyword_compare(dicts):
    # print(dicts['text'])
    for i in keywords:
        if i in dicts['text']:
            return 0
    return 1


def main():
    # 微博部分
    w = wbmonitor.weiboMonitor()
    w.getweiboInfo()
    with open(wbmonitor.COMPARE_FILE, 'r') as f:
        text = f.read()
        if text == '':
            w.getWBQueue()
    new_wb = w.startmonitor()
    if new_wb is not None:
        flag = keyword_compare(new_wb)
        if flag == 1:
            logging.info('准备推送')
            if 1:
                texts = push.pushChannels.telegram_HandleMessage(new_wb)
                push.pushChannels.telegram_Push(texts)  # 用telegram机器人推送
            # if 1:
            #     texts = push.pushChannels.wechat_HandleMessage(new_wb)
            #     push.pushChannels.wechat_Push(texts)  # 用企业微信推送

        else:
            print("没有关键词")
    else:
        # print("没有更新内容")
        logging.info('没有更新')


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(30)
