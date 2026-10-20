from flask import Blueprint
from my_project.controller import product_controller

# Створюємо "креслення" (Blueprint) для маршрутів товарів
products_bp = Blueprint('products_bp', __name__)

# З'єднуємо URL та методи (GET, POST, ...) з функціями контролера

products_bp.route('/products', methods=['GET'])(product_controller.get_all_products_controller)
products_bp.route('/products/<int:product_id>', methods=['GET'])(product_controller.get_product_by_id_controller)
products_bp.route('/products', methods=['POST'])(product_controller.create_product_controller)
products_bp.route('/products/<int:product_id>', methods=['PUT'])(product_controller.update_product_controller)
products_bp.route('/products/<int:product_id>', methods=['DELETE'])(product_controller.delete_product_controller)
products_bp.route('/products/<int:product_id>/attributes', methods=['GET'])(product_controller.get_product_attributes_controller)