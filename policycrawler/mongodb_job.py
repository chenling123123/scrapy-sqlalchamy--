#-*- coding: utf-8 -*-

from pymongo import MongoClient
from bson.objectid import ObjectId

class CMongo(object):
    def __init__(self):
        self.client = MongoClient('192.168.10.29',27017)
        #self.database = self.client["数据库"]
        #self.database.authenticate('账号','密码')
        self.dbs = self.client["python"]

    
    
    
    def add_one(self,collection_name,str):
        ''' 新增数据 '''


        return self.dbs[collection_name].insert_one(str)

    def get_one(self,collection_name,url):
        ''' 获取一条数据 '''
        return self.dbs[collection_name].find_one({'url':url})

    def get_more(self):
        ''' 查询多条数据 '''
        return self.db.find({})

    def get_one_from(self,oid):
        ''' 查询指定数据 '''
        obj = ObjectId(oid)
        return self.db.find_one({'_id':obj})

    def get_info(self,oid):
        ''' 条件查询统计 '''
        return self.db.find({'url':oid}).count()

    def get_count(self,oid):
        ''' 条件查询统计 '''
        return self.db.find(oid).count()


    def update(self,collection_name,url):
        '''更新数据'''

        return self.dbs[collection_name].update({'url':url},{"$set":{'state':1}})



