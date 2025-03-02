from functools import wraps
from flask import session, redirect, jsonify, url_for


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            return redirect("/login")

    return wrapper


# Decorator for role-based access control
def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "role" not in session:
                return redirect(
                    url_for("login")
                )  # Redirect to login if not logged in

            if session["role"] != role:
                return jsonify({"error": "Access Denied"}), 403  # Forbidden access

            return f(*args, **kwargs)

        return decorated_function

    return wrapper
