import redis

cache = redis.StrictRedis(host='localhost', port=6379, db=0)

def set_cache(key, value):
    cache.set(key, value)

def get_cache(key):
    return cache.get(key)
