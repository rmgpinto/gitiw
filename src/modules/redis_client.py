import os
import redis
import socket


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


def create_consumer_group():
  try:
    client().xgroup_create("webhooks", "webhooks-consumer-group", 0, mkstream=True)
  except Exception as e:
    if e.args[0] == "BUSYGROUP Consumer Group name already exists":
      pass
    else:
      raise e


def get_webhooks_from_stream():
  messages = client().xreadgroup(
      groupname="webhooks-consumer-group",
      consumername=socket.gethostname(),
      streams={"webhooks": ">"}
  )
  return messages


def delete_webhook_from_stream(webhook_id):
  client().xack("webhooks", "webhooks-consumer-group", webhook_id)
  client().xdel("webhooks", webhook_id)
