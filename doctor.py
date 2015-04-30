#coding=utf-8

import urllib2  
import urllib
import re  
import thread  
import time  

classes = dict()

#classesUrl = "http://health.sina.com.cn/d/2015-04-07/0837167340.shtml"
classesUrl = 'http://health.sina.com.cn/hc/ys/2015-04-03/0712168892.shtml'
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537 (KHTML, like Gecko) Chrome/38.0.21'

headers = { 'User-Agent': user_agent, 'Referer': 'http://health.sina.com.cn/' }

try:
    req = urllib2.Request(classesUrl, headers = headers) 
except urllib2.URLError, e:
    print e.reason

myResponse = urllib2.urlopen(req)
myPage = myResponse.read()

# if type(myPage).__name__!="unicode":
#     print 'not unicode'
#     myPage=myPage.decode("GB2312")


'''
abc = myPage.split('\n')
for i in abc:
    print i, '\n'
'''

#print myPage

#fp = open("x.html", 'r')
#myPage = fp.read()

lst = re.findall('<title>(.*?)</title>', myPage, re.S)
title = unicode(lst[0], "gb2312")
lst = re.findall('<meta name=keywords content="(.*?)">', myPage, re.S)
keywords = unicode(lst[0], "gb2312")
# for i in range(len(lst)):
# 	keywords.append(unicode(lst[0], "gb2312"))
keywords = unicode(lst[0], "gb2312")
lst = re.findall('<meta name=description content="(.*?)">', myPage, re.S)
description = unicode(lst[0], "gb2312")
lst = re.findall('<meta name="tags" content="(.*?)">', myPage, re.S)
tags = unicode(lst[0], "gb2312")
# for i in range(len(lst)):
# 	tags.append(unicode(lst[0], "gb2312"))

# print "title: ", title.split('_')[0]
# print "keywords: ", keywords.split(',')[0]
# print "description: ", description
# print "tags: ", tags.split(',')[0]

string = re.findall('<!-- publish_helper name=.*-->(.*?)<!-- publish_helper_end -->', myPage, re.S)

sss = unicode(string[0], "gb2312")
temp = re.findall('(<a.*?>)', sss, re.S);

for i in temp:
	print i

for i in temp:
	sss = sss.replace(i, '')
sss = sss.replace('</a>', '')

print sss


#items = re.findall('<dd><a href="(.*?)" target="_blank">(.*?)</a></dd>', myPage, re.S)
#items = re.findall('<dd><a href="(.*?)" target="_blank">(.*?)</a></dd>', myPage, re.S)

# for item in items:
#     print item[0], item[1]
    
links = [('疾病', 'http://health.sina.com.cn/disease/ku/'), ('常见病', 'http://health.sina.com.cn/cjb1/'), 
		 ('疑难病', 'http://health.sina.com.cn/ynb/'), ('生活', 'http://health.sina.com.cn/healthcare/'), 
		 ('幸福', 'http://health.sina.com.cn/sexknowledge/'), ('养生', 'http://health.sina.com.cn/hc/ct/'), 
		 ('提示', 'http://health.sina.com.cn/hc/sh/'), ('饮食', 'http://health.sina.com.cn/hc/ys/'), 
		 ('心理', 'http://health.sina.com.cn/hc/m/')]