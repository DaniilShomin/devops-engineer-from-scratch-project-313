import os

import sentry_sdk
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from database import Link, get_session, init_db

load_dotenv()

app = Flask(__name__)

sentry_dsn = os.environ.get("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

app.config["BASE_URL"] = os.environ.get("BASE_URL", "http://localhost:8080")
app.config["DATABASE_URL"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")


def make_short_url(short_name: str) -> str:
    base = app.config["BASE_URL"].rstrip("/")
    return f"{base}/r/{short_name}"


def link_to_dict(link: Link) -> dict:
    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "short_url": make_short_url(link.short_name),
    }


@app.route("/ping")
def ping():
    return "pong"


@app.route("/sentry-debug")
def trigger_error():
    division_by_zero = 1 / 0
    return division_by_zero


@app.route("/api/links", methods=["GET"])
def list_links():
    session = get_session()
    links = session.exec(select(Link)).all()
    session.close()
    return jsonify([link_to_dict(link) for link in links]), 200


@app.route("/api/links", methods=["POST"])
def create_link():
    data = request.get_json(silent=True) or {}
    original_url = data.get("original_url")
    short_name = data.get("short_name")

    if not original_url or not short_name:
        return jsonify({"error": "original_url and short_name are required"}), 422

    link = Link(original_url=original_url, short_name=short_name)
    session = get_session()
    session.add(link)
    try:
        session.commit()
        session.refresh(link)
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "short_name must be unique"}), 422
    finally:
        session.close()

    return jsonify(link_to_dict(link)), 201


@app.route("/api/links/<int:link_id>", methods=["GET"])
def get_link(link_id: int):
    session = get_session()
    link = session.get(Link, link_id)
    session.close()
    if not link:
        return jsonify({"error": "Not found"}), 404
    return jsonify(link_to_dict(link)), 200


@app.route("/api/links/<int:link_id>", methods=["PUT"])
def update_link(link_id: int):
    session = get_session()
    link = session.get(Link, link_id)
    if not link:
        session.close()
        return jsonify({"error": "Not found"}), 404

    data = request.get_json(silent=True) or {}
    original_url = data.get("original_url")
    short_name = data.get("short_name")

    if original_url is not None:
        link.original_url = original_url
    if short_name is not None:
        link.short_name = short_name

    try:
        session.add(link)
        session.commit()
        session.refresh(link)
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "short_name must be unique"}), 422
    finally:
        session.close()

    return jsonify(link_to_dict(link)), 200


@app.route("/api/links/<int:link_id>", methods=["DELETE"])
def delete_link(link_id: int):
    session = get_session()
    link = session.get(Link, link_id)
    if not link:
        session.close()
        return jsonify({"error": "Not found"}), 404

    session.delete(link)
    session.commit()
    session.close()
    return "", 204


if __name__ == "__main__":
    db_url = app.config["DATABASE_URL"]
    init_db(db_url)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
