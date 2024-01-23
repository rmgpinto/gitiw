import os
import redis
import socket
import time


REDIS_CLIENT = None


def init():
  globals()["REDIS_CLIENT"] = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, charset="utf-8", decode_responses=True)


def client():
  return globals()["REDIS_CLIENT"]


def send_webhook_to_stream(payload):
  response = client().xadd(os.getenv("REDIS_STREAM"), payload)
  if type(response) == str and len(response.split("-")) == 2:
    return True
  else:
    return False


def create_consumer_group():
  try:
    client().xgroup_create(os.getenv("REDIS_STREAM"), os.getenv("REDIS_CONSUMER_GROUP"), 0, mkstream=True)
  except Exception as e:
    if e.args[0] == "BUSYGROUP Consumer Group name already exists":
      pass
    else:
      raise e


def get_webhooks_from_stream():
  group_messages = client().xreadgroup(
      groupname=os.getenv("REDIS_CONSUMER_GROUP"),
      consumername=socket.gethostname(),
      streams={os.getenv("REDIS_STREAM"): ">"}
  )
  messages = []
  for message in group_messages:
    messages.append(message[1][0])
  return messages


def get_backend_server(client_id):
  server = client().get(f"backend:{client_id}")
  return server


def delete_webhook_from_stream(webhook_id):
  client().xack(os.getenv("REDIS_STREAM"), os.getenv("REDIS_CONSUMER_GROUP"), webhook_id)
  client().xdel(os.getenv("REDIS_STREAM"), webhook_id)


def get_pending_webhooks_from_stream(min_idle_time):
  pending_messages = client().xpending(
    name=os.getenv("REDIS_STREAM"),
    groupname=os.getenv("REDIS_CONSUMER_GROUP")
  )
  messages = []
  if pending_messages["pending"] > 0:
    min_pending_webhook_ts = int(pending_messages["min"].split("-")[0])
    webhook_age = (time.time() * 1000 - min_pending_webhook_ts)
    if webhook_age >= min_idle_time:
      pending_messages = client().xrange(
        name=os.getenv("REDIS_STREAM"),
        min=pending_messages["min"],
        max=pending_messages["min"]
      )
      if pending_messages:
        messages.append(pending_messages[0])
  return messages


def claim_pending_webhooks_from_stream(min_idle_time):
  messages = client().xautoclaim(
    name=os.getenv("REDIS_STREAM"),
    groupname=os.getenv("REDIS_CONSUMER_GROUP"),
    consumername=socket.gethostname(),
    min_idle_time=min_idle_time
  )
  return messages[1]
