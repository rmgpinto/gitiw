import json
import requests
from modules import redis_client
import time
import random


def send_webhook(webhook):
  try:
    webhook = json.loads(webhook)
    server = redis_client.get_backend_server(webhook["event-data"]["client-id"])
    response = requests.get(f"http://{server}", json=webhook)
    if response.status_code == 200:
      return True
    else:
      return False
  except Exception as e:
    return False


def send_webhook_exponential_backoff(webhook):
  retry = 0
  while retry <= 5:
    webhook_sent = webhooks_delivery.send_webhook(payload)
    if not webhook_sent:
      sleep = (5 * 2 ** retry + random.uniform(0, 1))
      time.sleep(sleep)
      retry += 1
