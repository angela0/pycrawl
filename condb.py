# encoding=utf-8

import pymongo

class ConnectDB():

    def __init__(self, host = 'localhost', port = 27017, db = 'health', collection = 'article'):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection


    def connectMongo(self):
        try:
            self.conn = pymongo.MongoClient(self.host, self.port, )

        except:
            print 'connect Mongo %s at port %d error'%(self.host, self.port)

    def useDb(self, db='health'):
        try:
            self.usedDb = self.conn[db]
        except:
            print 'connect db %s error'%(db)

    def useColl(self, collection='article'):
        try:
            self.usedColl = self.useDb[collection]
        except:
            print 'connect collection %s error'%(collection)

    def closeDB(self):
        self.conn.close()

cd = ConnectDB(host='123.123.123.123')

cd.connectMongo()


