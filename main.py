import json
import os

import sentry_sdk
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from database import Link, get_session, init_db

load_dotenv()

app = Flask(__name__)

CORS(
    app,
    origins=["http://localhost:5173"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Content-Range"],
    expose_headers=["Content-Range"],
)

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


def parse_range():
    range_param = request.args.get("range", "[0,10]")
    try:
        range_list = json.loads(range_param)
    except (json.JSONDecodeError, ValueError):
        return None

    if (
        not isinstance(range_list, list)
        or len(range_list) != 2
        or not isinstance(range_list[0], int)
        or not isinstance(range_list[1], int)
        or range_list[0] < 0
        or range_list[1] < 0
        or range_list[0] > range_list[1]
    ):
        return None

    return range_list[0], range_list[1]


@app.route("/ping")
def ping():
    return "pong"


@app.route("/sentry-debug")
def trigger_error():
    division_by_zero = 1 / 0
    return division_by_zero


@app.route("/api/links", methods=["GET"])
def list_links():
    parsed = parse_range()
    if parsed is None:
        return jsonify({"error": "Invalid range"}), 400

    start, end = parsed
    limit = end - start

    session = get_session()
    total = session.scalar(select(func.count()).select_from(Link)) or 0
    links = session.exec(select(Link).offset(start).limit(limit)).all()
    session.close()

    content_range = f"links {start}-{end}/{total}"
    response = jsonify([link_to_dict(link) for link in links])
    response.headers["Content-Range"] = content_range
    return response, 200


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
    db_url = app.config["DATABASE_URL"].replace("postgres://", "postgresql://", 1)
    init_db(db_url)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
