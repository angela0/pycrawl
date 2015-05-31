import pycurl
import StringIO
import chardet
import re
from collections import deque
import time
import pymongo


hashtable = []

try:
	conn = pymongo.MongoClient('localhost', 27017)
	db = conn.health
	coll = db.article
except:
	pass

def crawl(url, hashvalue):

	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	b = StringIO.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	# c.setopt(c.CURLOPT_SSL_VERIFYPEER, false);
	# c.setopt(c.CURLOPT_SSL_VERIFYHOST, false);
	c.setopt(c.TIMEOUT, 10)
	try :
		c.perform()
	except:
		print "see you next time!"
		return []

	string = b.getvalue()
	encoding = chardet.detect(string)['encoding']
	#string = unicode(string, encoding).encode('utf-8')
	#string = string.decode(encoding).encode('utf-8')
	keywords = u''
	description = u''
	title = u''
	text = u''

	links = re.findall('<a href="(.*?)".*>', string)

	temp = re.findall('<!-- publish_helper name=.*?-->(.*?)<!-- publish_helper_end -->', string, re.S)
	if len(temp)==0:
		return links
	try:
		text = unicode(temp[0], encoding).encode('utf-8')
	except:
		fp = open(str(hashvalue)+'.txt', 'w')
		fp.write(temp[0])
		fp.close()
		time.sleep(10000)

	temp = re.findall('<meta name=keywords content="(.*?)">', string)
	if len(temp)!=0:
		keywords = unicode(temp[0], encoding).encode('utf-8')

	temp = re.findall('<meta name=description content="(.*?)">', string)
	if len(temp)!=0:
		description = unicode(temp[0], encoding).encode('utf-8')

	temp = re.findall('<title>(.*?)</title>', string)
	if len(temp)!=0:
		title = unicode(temp[0], encoding).encode('utf-8')

	
	temp = re.findall('(<div.*</div>)', text, re.S)
	if len(temp)!=0:
		text = text.replace(temp[0], '')

	temp = re.findall('<a href=.*?>', text, re.S)
	for x in temp:
		text = text.replace(x, '')
	text = text.replace('</a>', '')


	data = {'_id':hashvalue, 'url':url, 'title':title, 'description':description, 'keywords':keywords, 'text':text}
	try:
		coll.insert(data)
	except:
		print 'insert error'


	# fp = open(str(hashvalue)+'.txt', 'w')
	# fp.write(url+title+description+keywords+text)
	# fp.close()
	

	
	return links



queue = deque(["http://health.sina.com.cn/disease/"])
#queue = deque(["http://health.sina.com.cn/d/2015-04-20/0947166366.shtml"])
while len(queue)!=0:
	cur = queue.pop()
	#print cur
	
	hashvalue = hash(cur)
	count = coll.find({'_id':hashvalue}).count()
	if count!=0:
		continue;

	hashtable.append(hashvalue)

	links = crawl(cur, hashvalue)
	if len(links)==0:
		print "over"
	else:
		for x in links:
			if x.startswith('http://health.sina.com.cn') and x.endswith('.shtml'):
				queue.append(x)
	#print hashtable
	time.sleep(1)
	
conn.close()