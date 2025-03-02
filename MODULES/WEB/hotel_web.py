from flask import Blueprint, redirect
from flask import render_template, jsonify
import logging

hotel_web = Blueprint("hotel_web", __name__, url_prefix="/hotel")


@hotel_web.route("/")
def index():
    return redirect("/hotel/dashboard")


@hotel_web.route("/login", methods=["GET"])
def hotel_login_page():
    try:
        return render_template("hotel_login_page.html")
    except Exception as e:
        logging.error("hotel_login_page", e)
        return jsonify({"error": "Loading failed"}), 302


@hotel_web.route("/dashboard", methods=["GET"])
def hotel_dashboard_page():
    try:
        return render_template("hotel_dashboard_page.html")
    except Exception as e:
        logging.error("hotel_dashboard_page", e)
        return jsonify({"error": "Loading failed"}), 302
