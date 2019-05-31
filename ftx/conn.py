import redis
from pymongo import MongoClient


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            cls.is_init = False
        return cls._instance


class Mongodb(Singleton):
    def __init__(self):
        try:
            self.conn = MongoClient(host='192.168.8.78', port=27017)
            self.db = self.conn['ftx']
        except:
            raise


class RedisClient(Singleton):

    def __init__(self):
        self.rds = redis.Redis(decode_responses=True)


conn = RedisClient()

