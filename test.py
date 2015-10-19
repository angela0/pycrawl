# encoding=utf-8
import pymongo

try:
    conn = pymongo.MongoClient('localhost', 27017)
    db = conn.health
    coll = db.article
except:
    print 'conn error'
    exit()

data = coll.find_one()

print data['title']