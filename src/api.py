import flask
from werkzeug.middleware.proxy_fix import ProxyFix
from modules import webhooks_inbound
from modules import redis_client


app = flask.Flask(__name__)
redis_client.init()


@app.route("/up", methods = ["GET"])
def up():
  return {"status": "healthy"}, 200


@app.route("/", methods = ["POST"])
def webhooks():
  response = webhooks_inbound.process(flask.request)
  return response
