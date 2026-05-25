import os

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(__name__)

# Инициализация Sentry, если задан SENTRY_DSN
sentry_dsn = os.environ.get("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


@app.route("/ping")
def ping():
    return "pong"


@app.route("/sentry-debug")
def trigger_error():
    division_by_zero = 1 / 0
    return division_by_zero


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
