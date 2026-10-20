from flask import jsonify, request
from my_project.service import category_service
def get_all_categories_controller():
    """GET /categories"""
    categories = category_service.get_all_categories()
    return jsonify(categories)

def get_category_by_id_controller(category_id):
    """GET /categories/<id>"""
    category = category_service.get_category_by_id(category_id)
    if category:
        return jsonify(category)
    return jsonify({"error": "Category not found"}), 404

def create_category_controller():
    """POST /categories"""
    data = request.json
    try:
        new_category = category_service.create_category(data)
        if new_category:
            return jsonify(new_category), 201
        return jsonify({"error": "Could not create category"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_category_controller(category_id):
    """PUT /categories/<id>"""
    data = request.json
    try:
        updated_category = category_service.update_category(category_id, data)
        if updated_category:
            return jsonify(updated_category), 200
        return jsonify({"error": f"Category not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_category_controller(category_id):
    """DELETE /categories/<id>"""
    try:
        deleted = category_service.delete_category(category_id)
        if deleted:
            return '', 204
        return jsonify({"error": f"Category not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500