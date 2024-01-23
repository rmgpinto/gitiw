from modules import redis_client
from modules import webhooks_delivery
import json
import os


if __name__ == "__main__":
  redis_client.init()
  redis_client.create_consumer_group()
  while True:
    webhooks = redis_client.get_webhooks_from_stream()
    for webhook in [*webhooks]:
      payload = webhook[1]["payload"]
      webhook_sent = webhooks_delivery.send_webhook(payload)
      if webhook_sent:
        webhook_id = webhook[0]
        redis_client.delete_webhook_from_stream(webhook_id)
