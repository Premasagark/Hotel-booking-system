import logging
from datetime import datetime
import requests
from flask import Blueprint, session, redirect, jsonify, request, url_for
from Config import db
import Config
from MODULES import AES
from MODULES.decorator import login_required


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def start_session(user, role):
    try:
        session["logged_in"] = True
        del user["password"]
        session["user"] = user
        session["role"] = role
        return jsonify({"msg": "Success"}), 200
    except Exception as e:
        return jsonify({"error"})


@auth_bp.route("/user/login/", methods=["POST"])
def user_login_api():
    try:
        form_data = request.json
        # normal user login
        if form_data["role"] == "user":
            user = db.users.find_one({"email": form_data['data']["email"]}, {"_id": 0})
            if not user :
                return jsonify({"error": "User not found"}), 404
            if user["password"] == AES.encrypt_password(
                form_data['data']["password"]
            ):
                user["last_login"] = datetime.now()
                db.users.update_one({"email": user["email"]}, {"$set": user})
                return start_session(user, form_data["role"])
        return {"error": "not logged in"}, 401
    except Exception as e:
        logging.error("user_login_api", e)
        return jsonify({"error": "login failed"}), 302


@auth_bp.route("/logout/")
@login_required
def logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as e:
        logging.error("logout", e)
        return {"error": "Error logging out"}, 302


@auth_bp.route("/user/signup/", methods=["POST"])
def user_signup_api():
    try:
        form_data = request.json
        if form_data["role"] == "user":
            user = db.users.find_one({"email": form_data['data']["email"]}, {"_id": 0})
            if not user:
                db.users.insert_one(
                    {
                        "username": form_data['data']["username"],
                        "email": form_data['data']["email"],
                        "password": AES.encrypt_password(form_data['data']["password"]),
                        "phone_number": form_data['data']["phone_number"],
                        "picture": None,
                        "last_login": None,
                    }
                )
                return jsonify({"msg": "User Created"}), 200
            else:
                return jsonify({"error": "User already exists"}), 999

        return jsonify({"error": "User Creation fail"}), 999

    except Exception as e:
        logging.error("user_signup_api", e)
        return {"error": "SignUp Failed"}, 302


# SIGN WITH GOOGLE
@auth_bp.route("/google/")
def login_with_google():
    try:
        auth_url = (
            f"{Config.AUTH_URL}?response_type=code&"
            f"client_id={Config.CLIENT_ID}&"
            f"redirect_uri={Config.REDIRECT_URL}&"
            f"scope={Config.SCOPE}&"
            f"access_type=offline"
        )
        # print(auth_url)
        return redirect(auth_url)
    except Exception as e:
        logging.error("login_with_google", e)
        return redirect("/login")


@auth_bp.route("/callback/")
def callback():
    try:
        code = request.args.get("code")
        token_response = requests.post(
            Config.TOKEN_URL,
            data={
                "code": code,
                "client_id": Config.CLIENT_ID,
                "client_secret": Config.CLIENT_SECRET,
                "redirect_uri": Config.REDIRECT_URL,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        # Get user info
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = user_info_response.json()
        print(user_info)

        if not user_info.get("email_verified"):
            raise Exception("Email not verified")

        # Check if user exists
        if not db.users.find_one({"email": user_info["email"]}):
            db.users.insert_one(
                {
                    "username": user_info["name"],
                    "email": user_info["email"],
                    "phone_number": None,
                    "picture": user_info["picture"],
                    "password": None,
                    "last_login": datetime.now(),
                }
            )
            

        # Store user information in session
        if user_info["email_verified"]:
            session["logged_in"] = True
            session["user"] = user_info
            session["role"] = "user"
        # return jsonify(user_info, {"msg": "Success"})
        return redirect("/home")
    except Exception as e:
        logging.error("callback", e)
        return redirect("/login")


# @auth_bp.route("/hotel/login", methods=["POST"])
# def hotel_login_api():
#     try:
#         form_data = request.form.get("data")
#         # hotel user login
#         if request.form.get("role") == "hotel":
#             hotel = db.hotels.find_one({"email": form_data.get("email")}, {"_id": 0})
#             if hotel and hotel["password"] == AES.encrypt_password(
#                 form_data.get("password")
#             ):
#                 hotel["last_login"] = str(datetime.now())
#                 db.users.update_one({"email": hotel["email"]}, {"$set": hotel})
#                 return start_session(hotel, request.form.get("role"))

#     except Exception as e:
#         logging.error("hotel_login_api" , e)
#         return redirect("/hotel/login", 302)


# @auth_bp.route("/hotel/signup", methods=["POST"])
# def hotel_signup_api():
#     try:
#         form_data = request.form.get("data")
#         if request.form.get("user_type") == "hotel":
#             hotel = db.hotels.find_one({"email": form_data.get("email")}, {"_id": 0})
#             if not hotel:
#                 form_data["picture"] = None
#                 form_data["last_login"] = None
#                 db.hotels.insert_one(form_data)
#                 return redirect("/hotel/login", 200)
#     except Exception as e:
#         logging.error("hotel_signup_api" + " ||| " + e)
#         return {"error": "SignUp Failed"}, 302
