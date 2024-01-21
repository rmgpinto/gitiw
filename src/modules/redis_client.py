import os
import redis
import socket


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


def send_webhook_to_dlq_stream(payload):
  response = client().xadd(os.getenv("REDIS_DLQ_STREAM"), payload)
  if type(response) == str and len(response.split("-")) == 2:
    return True
  else:
    return False


def create_consumer_group():
  try:
    client().xgroup_create(os.getenv("REDIS_STREAM") or os.getenv("REDIS_DLQ_STREAM"), os.getenv("REDIS_CONSUMER_GROUP") or os.getenv("REDIS_DLQ_CONSUMER_GROUP"), 0, mkstream=True)
  except Exception as e:
    if e.args[0] == "BUSYGROUP Consumer Group name already exists":
      pass
    else:
      raise e


def get_webhooks_from_stream():
  messages = client().xreadgroup(
      groupname=os.getenv("REDIS_CONSUMER_GROUP") or os.getenv("REDIS_DLQ_CONSUMER_GROUP"),
      consumername=socket.gethostname(),
      streams={os.getenv("REDIS_STREAM") or os.getenv("REDIS_DLQ_STREAM"): ">"}
  )
  return messages


def get_backend_server(client_id):
  server = client().get(f"backend:{client_id}")
  return server


def delete_webhook_from_stream(webhook_id):
  client().xack(os.getenv("REDIS_STREAM") or os.getenv("REDIS_DLQ_STREAM"), os.getenv("REDIS_CONSUMER_GROUP") or os.getenv("REDIS_DLQ_CONSUMER_GROUP"), webhook_id)
  client().xdel(os.getenv("REDIS_STREAM") or os.getenv("REDIS_DLQ_STREAM"), webhook_id)
