from flask import jsonify, request
from my_project.service import review_service

def get_all_reviews_controller():
    """GET /reviews"""
    reviews = review_service.get_all_reviews()
    return jsonify(reviews)

def get_review_by_id_controller(review_id):
    """GET /reviews/<id>"""
    review = review_service.get_review_by_id(review_id)
    if review:
        return jsonify(review)
    return jsonify({"error": "Review not found"}), 404

def create_review_controller():
    """POST /reviews"""
    data = request.json
    
    # Перевірка наявності потрібних полів
    required_fields = ['rating', 'Users_id', 'Products_id']
    if not data or not all(field in data for field in required_fields):
         return jsonify({"error": "Missing 'rating', 'Users_id', or 'Products_id'"}), 400
         
    try:
        new_review = review_service.create_review(data)
        if new_review:
            return jsonify(new_review), 201
        return jsonify({"error": "Could not create review"}), 400
    except Exception as e:
        # Може статися, якщо Users_id або Products_id не існує
        return jsonify({"error": str(e)}), 500

def update_review_controller(review_id):
    """PUT /reviews/<id>"""
    data = request.json
    try:
        updated_review = review_service.update_review(review_id, data)
        if updated_review:
            return jsonify(updated_review), 200
        return jsonify({"error": f"Review not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_review_controller(review_id):
    """DELETE /reviews/<id>"""
    try:
        deleted = review_service.delete_review(review_id)
        if deleted:
            return '', 204
        return jsonify({"error": f"Review not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500