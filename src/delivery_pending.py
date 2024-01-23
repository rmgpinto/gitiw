from modules import redis_client
from modules import webhooks_delivery
import json
import os
import time


if __name__ == "__main__":
  redis_client.init()
  redis_client.create_consumer_group()
  while True:
    pending_webhooks = redis_client.get_pending_webhooks_from_stream(10000)
    pending_webhooks_claimed = redis_client.claim_pending_webhooks_from_stream(10000)
    for webhook in [*pending_webhooks, *pending_webhooks_claimed]:
      if webhook:
        webhook_sent = webhooks_delivery.send_webhook_exponential_backoff(webhook[1]["payload"])
        webhook_id = webhook[0]
        redis_client.delete_webhook_from_stream(webhook_id)
    else:
      time.sleep(5)
