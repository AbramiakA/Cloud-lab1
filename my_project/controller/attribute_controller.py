from flask import jsonify, request
from my_project.service import attribute_service

def get_all_attributes_controller():
    """GET /attributes"""
    attributes = attribute_service.get_all_attributes()
    return jsonify(attributes)

def get_attribute_by_id_controller(attribute_id):
    """GET /attributes/<id>"""
    attribute = attribute_service.get_attribute_by_id(attribute_id)
    if attribute:
        return jsonify(attribute)
    return jsonify({"error": "Attribute not found"}), 404

def create_attribute_controller():
    """POST /attributes"""
    data = request.json
    try:
        new_attribute = attribute_service.create_attribute(data)
        if new_attribute:
            return jsonify(new_attribute), 201
        return jsonify({"error": "Could not create attribute"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_attribute_controller(attribute_id):
    """PUT /attributes/<id>"""
    data = request.json
    try:
        updated_attribute = attribute_service.update_attribute(attribute_id, data)
        if updated_attribute:
            return jsonify(updated_attribute), 200
        return jsonify({"error": f"Attribute not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_attribute_controller(attribute_id):
    """DELETE /attributes/<id>"""
    try:
        deleted = attribute_service.delete_attribute(attribute_id)
        if deleted:
            return '', 204
        return jsonify({"error": f"Attribute not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500