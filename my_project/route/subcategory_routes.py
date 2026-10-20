# --- my_project/route/subcategory_routes.py ---

from flask import Blueprint
from my_project.controller import subcategory_controller

subcategories_bp = Blueprint('subcategories_bp', __name__)

# /api/subcategories
subcategories_bp.route('/subcategories', methods=['GET'])(subcategory_controller.get_all_subcategories_controller)
subcategories_bp.route('/subcategories', methods=['POST'])(subcategory_controller.create_subcategory_controller)

# /api/subcategories/5
subcategories_bp.route('/subcategories/<int:subcategory_id>', methods=['GET'])(subcategory_controller.get_subcategory_by_id_controller)
subcategories_bp.route('/subcategories/<int:subcategory_id>', methods=['PUT'])(subcategory_controller.update_subcategory_controller)
subcategories_bp.route('/subcategories/<int:subcategory_id>', methods=['DELETE'])(subcategory_controller.delete_subcategory_controller)