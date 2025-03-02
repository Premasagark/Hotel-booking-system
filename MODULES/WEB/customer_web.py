import logging
from MODULES.decorator import login_required, role_required

from flask import Blueprint
from flask import render_template, redirect, jsonify, request

cust_web = Blueprint("customer_web", __name__)


@cust_web.route("/login/", methods=["GET"])
def user_login_page():
    try:
        return render_template("user_login.html")
    except Exception as e:
        logging.error("user_login_page", e)
        return jsonify({"error": "Loading failed"}), 302


@cust_web.route("/home/", methods=["GET"])
@login_required
@role_required("user")
def user_home_page():
    try:
        return render_template("users_home_page.html")
    except Exception as e:
        logging.error("user_login_page", e)
        return jsonify({"error": "Loading failed"}), 302

@cust_web.route("/view/hotel/", methods=["GET"])
@login_required
@role_required("user")
def view_hotel_page():
    try:
        hotel_id = request.args.get("hotel_id")
        return render_template("hotel_booking.html",hotel_id = hotel_id)
    except Exception as e:
        logging.error("view_hotel", e)
        return jsonify({"error": "Loading failed"}), 302