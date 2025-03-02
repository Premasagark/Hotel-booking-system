from flask import Blueprint, jsonify, request
from MODULES.decorator import login_required, role_required
from Config import db
from bson import ObjectId
from bson.json_util import dumps

import logging


search_hotel_bp = Blueprint("search_hotel", __name__, url_prefix="/search")


@search_hotel_bp.route("/hotel/", methods=["POST"])
@login_required
@role_required("user")
def search_hotel():
    try:
        form_data = request.json
        page = int(request.args.get('page', 1))  # Default to page 1
        items_per_page = int(request.args.get('items_per_page', 10))  # Default to 10 items per page
    
        skip = (page - 1) * items_per_page
        search_query = form_data["data"]["search_query"].strip()

        hotel = db.hotels.find(
            {
                "$or": [
                    {"hotel_name": {"$regex": search_query, "$options": "i"}},
                    {"location.city": {"$regex": search_query, "$options": "i"}},
                    {"location.state": {"$regex": search_query, "$options": "i"}},
                    {"location.country": {"$regex": search_query, "$options": "i"}},
                ]
            },
            {
                "_id": 1,
                "hotel_name": 1,
                "location": 1,
                "rating": 1,
                "description": 1,
                "services": 1,
                "hotel_images": 1,
                "base_price": 1,
            },
        ).skip(skip).limit(items_per_page)

        if not hotel:
            return jsonify({"error": "Hotel not found"}), 302
        list_hotel = list(hotel)
        list_hotel = [[{**doc, "_id": str(doc["_id"])} for doc in list_hotel]]
        return jsonify({"hotel_list": list_hotel}), 200
    except Exception as e:
        logging.error("search_hotel", e)
        return jsonify({"error": "Error searching hotel"}), 302


@search_hotel_bp.route("/view/hotel/", methods=["POST"])
@login_required
@role_required("user")
def detail_hotel():
    try:
        form_data = request.json
        hotel = db.hotels.find_one({"_id": ObjectId(form_data['hotel_id'])})
        if not hotel:
            return jsonify({"error": "Hotel not found"}), 302
        hotel = {**hotel, "_id": str(hotel["_id"])}
        return jsonify({"hotel": hotel}), 200
    except Exception as e:
        logging.error("detail_hotel", e)
        return jsonify({"error": "Error getting hotel"}), 302