from Config import db
from MODULES.decorator import login_required, role_required
import logging
from flask import Blueprint, jsonify, request, session, render_template
from datetime import datetime
from bson import ObjectId

booking_bp = Blueprint("booking", __name__, url_prefix="/booking")


@booking_bp.route("/room/", methods=["POST"])
@login_required
@role_required("user")
def booking_hotel_api():
    try:
        form_data = request.json
        form_data["hotel_id"] = ObjectId(form_data["hotel_id"])
        hotel = db.hotels.find_one({"_id": form_data["hotel_id"]})
        if not hotel:
            return jsonify({"error": "Hotel not found"}), 302

        form_data["user_email"] = session["user"]["email"]
        form_data["created_at"] = datetime.now()
        data = form_data
        db.hotel_booking.insert_one(data)

        return jsonify({"msg": "Success"}), 200
    except Exception as e:
        logging.error("booking_hotel", exc_info=True)
        return jsonify({"error": "Hotel booking failed"}), 302


# @booking_bp.route("/view/", methods=["POST"])
# @login_required
# @role_required("user")
# def view_booking_api():
#     try:
#         user_email = session["user"]["email"]
#         booking = db.hotel_booking.find({"user_email": user_email})
#         if not booking:
#             return jsonify({"error": "Booking not found"}), 302
#         list_booking = list(booking)
#         list_booking = [{**doc, "_id": str(doc["_id"]), "hotel_id": str(doc['hotel_id']), "created_at": str(doc['created_at'])} for doc in list_booking]
#         return jsonify({"booking_list": list_booking}), 200
#     except Exception as e:
#         logging.error("view_booking", e)
#         return jsonify({"error": "Error viewing booking"}), 302


@booking_bp.route("/view/", methods=["POST"])
@login_required
@role_required("user")
def view_booking_api():
    try:
        user_email = session["user"]["email"]
        booking = db.hotel_booking.aggregate(
            [
                {"$match": {"user_email": user_email}},
                {
                    "$lookup": {
                        "from": "hotels",  # Name of the hotels collection
                        "localField": "hotel_id",
                        "foreignField": "_id",
                        "as": "hotel_details",
                    }
                },
                {
                    "$unwind": {  # Unwind the array to get a single hotel document
                        "path": "$hotel_details",
                        "preserveNullAndEmptyArrays": True,
                    }
                },
            ]
        )

        list_booking = list(booking)
        if not list_booking:
            return jsonify({"error": "Booking not found"}), 302

        # Format the response
        formatted_booking = [
            {
                **doc,
                "_id": str(doc["_id"]),
                "hotel_id": str(doc["hotel_id"]),
                "created_at": str(doc["created_at"]),
                "hotel_name": (
                    str(doc["hotel_details"]["hotel_name"])
                    if "hotel_details" in doc
                    else "N/A"
                ),
                "hotel_details": {
                    **doc["hotel_details"],
                    "_id": str(doc["hotel_details"]["_id"]),
                },
            }
            for doc in list_booking
        ]

        return jsonify({"booking_list": formatted_booking}), 200

    except Exception as e:
        logging.error("view_booking", exc_info=True)
        return jsonify({"error": "Error viewing booking"}), 302


@booking_bp.route("/view/", methods=["GET"])
@login_required
@role_required("user")
def view_booking():
    try:
        return render_template("view_booking.html")
    except Exception as e:
        logging.error("view_booking", exc_info=True)
        return jsonify({"error": "Error viewing booking"}), 302
