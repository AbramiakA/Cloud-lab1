from flask import current_app, jsonify, request
from my_project.service import product_idempotency, product_service

def _server_error(operation):
    current_app.logger.exception("Product API error: %s", operation)
    return jsonify({"error": "Internal server error"}), 500


def get_all_products_controller():
    """GET /api/products?page=1&limit=20 (max limit: 100)."""
    try:
        page = int(request.args.get("page", "1"))
        limit = int(request.args.get("limit", "20"))
    except (ValueError, TypeError):
        return jsonify({"error": "page and limit must be integers"}), 400

    if page < 1 or not 1 <= limit <= 100:
        return jsonify({"error": "page must be >= 1 and limit must be 1..100"}), 400

    try:
        return jsonify(product_service.get_all_products(page=page, limit=limit))
    except Exception:
        return _server_error("list products")


def get_product_by_id_controller(product_id):
    try:
        product, cache_status = product_service.get_cached_product_by_id(product_id)

        if product is None:
            return jsonify({"error": "Product not found"}), 404

        response = jsonify(product)
        response.headers["X-Cache"] = cache_status
        return response
    except Exception:
        return _server_error("get product")


def create_product_controller():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    try:
        key = request.headers.get("Idempotency-Key")

        if key is None:
            new_product = product_service.create_product(data)
            return jsonify(new_product), 201

        product, status = product_idempotency.create_once(
            key,
            data,
            product_service.create_product
        )

        return jsonify(product), status

    except product_idempotency.IdempotencyError as error:
        response = jsonify({"error": str(error)})

        if str(error) == "Request already in progress":
            response.headers["Retry-After"] = "1"

        return response, error.status_code

    except Exception:
        return _server_error("create product")


def update_product_controller(product_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON object"}), 400

    try:
        updated_product = product_service.update_product(product_id, data)
        if updated_product is None:
            return jsonify({"error": "Product not found or no changes made"}), 404
        return jsonify(updated_product), 200
    except Exception:
        return _server_error("update product")


def delete_product_controller(product_id):
    try:
        deleted = product_service.delete_product(product_id)
        if deleted:
            return "", 204
        return jsonify({"error": "Product not found"}), 404
    except Exception:
        return _server_error("delete product")


def get_product_attributes_controller(product_id):
    try:
        attributes = product_service.get_product_attributes(product_id)
        return jsonify(attributes), 200
    except Exception:
        return _server_error("get product attributes")
