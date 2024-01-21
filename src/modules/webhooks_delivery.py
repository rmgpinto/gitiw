import json
import requests
from modules import redis_client


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
