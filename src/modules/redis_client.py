import os
import redis


REDIS_CLIENT = None


def init():
  globals()["REDIS_CLIENT"] = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, charset="utf-8", decode_responses=True)


def client():
  return globals()["REDIS_CLIENT"]


def send_webhook_to_stream(stream, payload):
  response = client().xadd(stream, payload)
  if type(response) == str and len(response.split("-")) == 2:
    return True
  else:
    return False
