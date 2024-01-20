import flask
from werkzeug.middleware.proxy_fix import ProxyFix
from modules import webhooks_inbound


app = flask.Flask(__name__)


@app.route("/up", methods = ["GET"])
def up():
  return {"status": "healthy"}, 200


@app.route("/", methods = ["POST"])
def webhooks():
  response = webhooks_inbound.process(flask.request)
  return response
