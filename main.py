#coding=utf-8


import doctor

links = [('疾病', 'http://health.sina.com.cn/disease/ku/'), ('常见病', 'http://health.sina.com.cn/cjb1/'), 
		 ('疑难病', 'http://health.sina.com.cn/ynb/'), ('生活', 'http://health.sina.com.cn/healthcare/'), 
		 ('幸福', 'http://health.sina.com.cn/sexknowledge/'), ('养生', 'http://health.sina.com.cn/hc/ct/'), 
		 ('提示', 'http://health.sina.com.cn/hc/sh/'), ('饮食', 'http://health.sina.com.cn/hc/ys/'), 
		 ('心理', 'http://health.sina.com.cn/hc/m/')]


'''
for url in links:
	results = doctor.crawl(url[1], "article")
	print results

results = doctor.crawl("http://health.sina.com.cn/d/2015-03-04/0736167107.shtml", "article")
if results:
	print results[0].encode("utf-8")
'''

results = doctor.crawl("http://health.sina.com.cn/hc/ys/", "url")
