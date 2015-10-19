# coding=utf-8
import pycurl
import StringIO
import chardet
import re
from collections import deque
import pymongo
import time
from lxml import html

hashtable = []
html_tags = ['div', 'span', 'style', 'script']

try:
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.health
    coll = db.disease
except:
    print 'conn error'
    exit()


def crawl(url, hashvalue):

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

    doc = html.fromstring(string)
    links = doc.xpath('//a/attribute::href')

    temp = re.findall('<!--C_box1 start-->(.*?)<!--C_box1 end-->', string, re.S)
    if len(temp) == 0:
        return links
    try:
        text = unicode(temp[0], encoding, 'ignore')
    except:
        print 'decode error', url
        #time.sleep(1)


    title = doc.xpath('//title/text()')[0]
    title = title.split('_')[0]

    keywords = doc.xpath('//meta[@name="Keywords"]/attribute::content')[0]
    keywords = keywords.split(',')[0]

    description = doc.xpath('//meta[@name="Description"]/attribute::content')[0]

    doc = html.fromstring(text)

    survey = doc.xpath('//div[@class="box_txt"]/ul/child::*/text()')

    dsurvey = doc.xpath('//div[@class="box_txt"]/dl[1]/dd/text()')


    show = doc.xpath('//div[@class="box_txt"]/dl[2]/dd/text()')

    pre = doc.xpath('//div[@class="box_txt"]/dl[3]/dd/text()')

    #text = delt_text(text)

    data = {'_id': hashvalue, 'url': url, 'title': title, 'description': description, 'keywords': keywords,
            '疾病概况': survey[0], '疾病概述': dsurvey[0], '临床表现': show[0], '疾病防治': pre[0]}
    try:
        coll.insert(data)
        print 'yes'
    except:
        print 'insert error'

    # fp = open(str(hashvalue)+'.txt', 'w')
    # fp.write(url+title+description+keywords+text)
    # fp.close()

    return links


queue = deque(["http://health.sina.com.cn/disease/ku/"])
#queue = deque(["http://health.sina.com.cn/d/2012-03-20/160824567.shtml"])
while len(queue) != 0:

    cur = queue.pop()
    print cur
    hashvalue = hash(cur)
    count = coll.find({'_id': hashvalue}).count()
    if count != 0:
        continue


    hashtable.append(hashvalue)

    links = crawl(cur, hashvalue)

    if links==[]:
        print "over"
    else:
        for x in links:
            hashvalue = hash(x)
            count = coll.find({'_id': hashvalue}).count()

            if x.startswith('http://health.sina.com.cn/disease/ku/') or x.startswith('http://health.sina.com.cn/disease/department') and count==0:
                queue.append(x)
    #time.sleep(1)

print time.asctime()
conn.close()
