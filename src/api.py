from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

@app.route("/up")
def up():
  return {"status": "healthy"}, 200
