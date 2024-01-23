from modules import redis_client
from modules import webhooks_delivery
import json
import os


if __name__ == "__main__":
  redis_client.init()
  redis_client.create_consumer_group()
  while True:
    webhooks = redis_client.get_webhooks_from_stream()
    for webhook in webhooks:
      payload = webhook[1][0][1]["payload"]
      webhook_sent = webhooks_delivery.send_webhook(payload)
      if webhook_sent:
        webhook_id = webhook[1][0][0]
        redis_client.delete_webhook_from_stream(webhook_id)
      else:
        if not os.getenv("DELIVERY_DLQ"):
          redis_client.send_webhook_to_dlq_stream({ "payload": json.dumps(payload) })
        else:
          webhooks_delivery.send_webhook_exponential_backoff(payload)
