import requests


def send_webhook(webhook):
  try:
    response = requests.get("http://echoserver", json=webhook)
    if response.status_code == 200:
      return True
    else:
      return False
  except Exception as e:
    return False
