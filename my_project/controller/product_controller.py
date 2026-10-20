from flask import jsonify, request
from my_project.service import product_service

def get_all_products_controller():
    """GET /products"""
    products = product_service.get_all_products()
    return jsonify(products)

def get_product_by_id_controller(product_id):
    """GET /products/<id>"""
    product = product_service.get_product_by_id(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

def create_product_controller():
    """POST /products"""
    data = request.json
    try:
        new_product = product_service.create_product(data)
        if new_product:
            return jsonify(new_product), 201 # 201 = Created
        return jsonify({"error": "Could not create product"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_product_controller(product_id):
    """PUT /products/<id>"""
    data = request.json
    try:
        updated_product = product_service.update_product(product_id, data)
        if updated_product:
            return jsonify(updated_product), 200
        return jsonify({"error": f"Product not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_product_controller(product_id):
    """DELETE /products/<id>"""
    try:
        deleted = product_service.delete_product(product_id)
        if deleted:
            return '', 204 # 204 = No Content (успішне видалення)
        return jsonify({"error": f"Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def get_product_attributes_controller(product_id):
    """GET /products/<id>/attributes"""
    try:
        attributes = product_service.get_product_attributes(product_id)
        return jsonify(attributes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
