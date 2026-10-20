from flask import jsonify, request
from my_project.service import user_service

def get_all_users_controller():
    """GET /users"""
    users = user_service.get_all_users()
    return jsonify(users)

def get_user_by_id_controller(user_id):
    """GET /users/<id>"""
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

def create_user_controller():
    """POST /users"""
    data = request.json
    try:
        new_user = user_service.create_user(data)
        if new_user:
            return jsonify(new_user), 201 # 201 = Created
        return jsonify({"error": "Could not create user"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_user_controller(user_id):
    """PUT /users/<id>"""
    data = request.json
    try:
        updated_user = user_service.update_user(user_id, data)
        if updated_user:
            return jsonify(updated_user), 200
        return jsonify({"error": f"User not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_user_controller(user_id):
    """DELETE /users/<id>"""
    try:
        deleted = user_service.delete_user(user_id)
        if deleted:
            return '', 204 # 204 = No Content
        return jsonify({"error": f"User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500