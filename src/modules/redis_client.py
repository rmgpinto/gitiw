import redis


REDIS_CLIENT = None


def client():
  return globals()["REDIS_CLIENT"]


def init():
  globals()["REDIS_CLIENT"] = redis.Redis(host="redis", port=6379)
