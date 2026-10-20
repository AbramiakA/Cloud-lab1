from flask import jsonify, request
from my_project.service import subcategory_service

def get_all_subcategories_controller():
    """GET /subcategories"""
    subcategories = subcategory_service.get_all_subcategories()
    return jsonify(subcategories)

def get_subcategory_by_id_controller(subcategory_id):
    """GET /subcategories/<id>"""
    subcategory = subcategory_service.get_subcategory_by_id(subcategory_id)
    if subcategory:
        return jsonify(subcategory)
    return jsonify({"error": "Subcategory not found"}), 404

def create_subcategory_controller():
    """POST /subcategories"""
    data = request.json
    
    # Перевірка наявності обох полів
    if not data or 'name' not in data or 'Categories_id' not in data:
         return jsonify({"error": "Missing 'name' or 'Categories_id'"}), 400
         
    try:
        new_subcategory = subcategory_service.create_subcategory(data)
        if new_subcategory:
            return jsonify(new_subcategory), 201
        return jsonify({"error": "Could not create subcategory"}), 400
    except Exception as e:
        # Може статися, якщо Categories_id не існує (помилка Foreign Key)
        return jsonify({"error": str(e)}), 500

def update_subcategory_controller(subcategory_id):
    """PUT /subcategories/<id>"""
    data = request.json
    try:
        updated_subcategory = subcategory_service.update_subcategory(subcategory_id, data)
        if updated_subcategory:
            return jsonify(updated_subcategory), 200
        return jsonify({"error": f"Subcategory not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_subcategory_controller(subcategory_id):
    """DELETE /subcategories/<id>"""
    try:
        deleted = subcategory_service.delete_subcategory(subcategory_id)
        if deleted:
            return '', 204
        return jsonify({"error": f"Subcategory not found"}), 404
    except Exception as e:
        # Може статися, якщо товари посилаються на цю підкатегорію
        return jsonify({"error": str(e)}), 500