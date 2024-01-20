import jsonschema


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


def process(request):
  if not validate_schema(request):
    return {"message": "Invalid JSON schema."}, 400
  payload = request.get_json()
  if not validate_payload(payload):
    return {"message": "Invalid JSON payload."}, 400
  return {"message": "Webhook accepted."}, 200
