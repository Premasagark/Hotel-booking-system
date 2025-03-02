from flask import Flask, redirect

from datetime import timedelta
import Config
import os


from MODULES.API.auth import auth_bp
# from MODULES.WEB.hotel_web import hotel_web
from MODULES.WEB.customer_web import cust_web
from MODULES.API.search_hotel import search_hotel_bp
from MODULES.API.booking_api import booking_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "the secret key")
# Set session lifetime (e.g., 30 minutes)
app.permanent_session_lifetime = timedelta(minutes=int(Config.expiry_time))

# Blueprints
app.register_blueprint(auth_bp)
# app.register_blueprint(hotel_web)
app.register_blueprint(cust_web)
app.register_blueprint(search_hotel_bp)
app.register_blueprint(booking_bp)


@app.route("/")
def index():  # put application's code here
    return redirect("/home")


# if __name__ == "__main__":
#     app.run(debug=True)
