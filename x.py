# coding=utf-8
import pycurl
import StringIO
import chardet
import re
from collections import deque
import pymongo
import time

hashtable = []
html_tags = ['div', 'span', 'style', 'script']

try:
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.health
    coll = db.article
except:
    print 'conn error'
    exit()


def delt_text(text):

    for i in html_tags:
        if text.find(i)!=-1:
            tmp = re.findall('(<'+i+'.*?</'+i+'>)', text, re.S)
            for j in tmp:
                text = text.replace(j, '')

    tmp = re.findall('(<!--.*?-->)', text, re.S)
    for j in tmp:
        text = text.replace(j, '')

    temp = re.findall('<a href=.*?>', text, re.S)
    for j in temp:
        text = text.replace(j, '')
    text = text.replace('</a>', '')

    return text


def crawl(url, hashvalue):
    print 'come in '
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    # c.setopt(c.CURLOPT_SSL_VERIFYPEER, false);
    # c.setopt(c.CURLOPT_SSL_VERIFYHOST, false);
    c.setopt(c.TIMEOUT, 10)
    try:
        c.perform()
    except:
        print "see you next time!"
        print url
        return []


    string = b.getvalue()
    encoding = chardet.detect(string)['encoding']
    # string = unicode(string, encoding).encode('utf-8')
    # string = string.decode(encoding).encode('utf-8')

    keywords = description = title = text = u''

    links = re.findall('<a href="(.*?)".*>', string)

    temp = re.findall('<!-- publish_helper name=.*?-->(.*?)<!-- publish_helper_end -->', string, re.S)
    if len(temp) == 0:
        return links

    try:
        text = unicode(temp[0], encoding, 'ignore')
    except:
        print 'decode error', url
        #time.sleep(1)

    temp = re.findall('<meta name=keywords content="(.*?)">', string)
    if len(temp) != 0:
        keywords = unicode(temp[0], encoding, 'ignore').encode('utf-8')

    temp = re.findall('<meta name=description content="(.*?)">', string)
    if len(temp) != 0:
        description = unicode(temp[0], encoding, 'ignore').encode('utf-8')

    temp = re.findall('<title>(.*?)</title>', string)
    if len(temp) != 0:
        title = unicode(temp[0], encoding, 'ignore').encode('utf-8')
        title = title.split('_')[0]

    temp = re.findall('(<div.*</div>)', text, re.S)
    if len(temp) != 0:
        text = text.replace(temp[0], '')

    text = delt_text(text)

    print 'here'
    data = {'_id': hashvalue, 'url': url, 'title': title, 'description': description, 'keywords': keywords,
            'text': text}
    try:
        coll.insert(data)
        print 'yes'
    except:
        print 'insert error'

    # fp = open(str(hashvalue)+'.txt', 'w')
    # fp.write(url+title+description+keywords+text)
    # fp.close()

    return links


queue = deque(["http://health.sina.com.cn/disease/"])
#queue = deque(["http://health.sina.com.cn/d/2012-03-20/160824567.shtml"])
while len(queue) != 0:

    cur = queue.pop()
    print cur
    hashvalue = hash(cur)
    count = coll.find({'_id': hashvalue}).count()
    if count != 0:
        print 'exits'
        continue

    hashtable.append(hashvalue)

    links = crawl(cur, hashvalue)

    if links==[]:
        print "over"
    else:
        for x in links:
            hashvalue = hash(x)
            count = coll.find({'_id': hashvalue}).count()

            if x.startswith('http://health.sina.com.cn') and x.endswith('.shtml') and count==0:
                queue.append(x)
    time.sleep(1)

print time.asctime()
conn.close()
