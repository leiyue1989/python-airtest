import redis
from common import tools

env = tools.getEnv()
if env == "local":
    redis_conn = redis.Redis(host='192.168.0.143', port=6079, password='', db=0)
elif env == "lazy" or env == "test":
    redis_conn = redis.Redis(host='192.168.0.143', port=6079, password='', db=0)
else:
    redis_conn = redis.Redis(host='192.168.110.222', port=6379, password='', db=0)


class RedisDB(object):

    @staticmethod
    def getKey(key):
        return redis_conn.get(key)

    @staticmethod
    def setKey(key, val):
        redis_conn.set(key, val)

    @staticmethod
    def delKey(key):
        return redis_conn.delete(key)

    @staticmethod
    def incr(key, expire_time=3600):
        if redis_conn.exists(key):
            return redis_conn.incr(key, 1)
        else:
            count = redis_conn.incr(key, 1)
            redis_conn.expire(key, expire_time)
            return count

    @staticmethod
    def ttl(key):
        return redis_conn.ttl(key)

    @staticmethod
    def expireTime(key, expire_time=3600):
        return redis_conn.expire(key, expire_time)
