from flask import Blueprint
from my_project.controller import category_controller

categories_bp = Blueprint('categories_bp', __name__)

# /api/categories
categories_bp.route('/categories', methods=['GET'])(category_controller.get_all_categories_controller)
categories_bp.route('/categories', methods=['POST'])(category_controller.create_category_controller)

# /api/categories/5
categories_bp.route('/categories/<int:category_id>', methods=['GET'])(category_controller.get_category_by_id_controller)
categories_bp.route('/categories/<int:category_id>', methods=['PUT'])(category_controller.update_category_controller)
categories_bp.route('/categories/<int:category_id>', methods=['DELETE'])(category_controller.delete_category_controller)