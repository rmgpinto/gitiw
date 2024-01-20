import jsonschema
from modules import redis_client
import json


schema = {
  "type": "object",
  "properties": {
    "signature": {
      "type": "object",
      "properties": {
        "timestamp": {"type": "string"},
        "token": {"type": "string"},
        "signature": {"type": "string"}
      }
    }
  },
  "event-data": {
    "type": "object",
    "properties": {
      "event": {"type": "string"},
      "timestamp": {"type": "integer"},
      "id": {"type": "string"}
    }
  }
}


def validate_schema(request):
  try:
    return request.get_json()
  except Exception as e:
    return False


def validate_payload(payload):
  try:
    jsonschema.validate(instance=payload, schema=schema)
    return True
  except Exception as e:
    return False


def send_message_to_stream(payload):
  response = redis_client.client().xadd(
    "webhooks",
    { "payload": json.dumps(payload) }
  )
  if type(response) == bytes and len(response.decode("utf-8").split("-")) == 2:
    return True
  else:
    return False



def process(request):
  is_valid_schema = validate_schema(request)
  if not is_valid_schema:
    return {"message": "Invalid JSON schema."}, 400
  payload = request.get_json()
  is_valid_payload = validate_payload(payload)
  if not is_valid_payload:
    return {"message": "Invalid JSON payload."}, 400
  is_message_sent_to_stream = send_message_to_stream(payload)
  if not is_message_sent_to_stream:
    return {"message": "Unable to process webhook."}, 500
  return {"message": "Webhook accepted."}, 200
