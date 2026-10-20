# --- my_project/route/attribute_routes.py ---

from flask import Blueprint
from my_project.controller import attribute_controller

attributes_bp = Blueprint('attributes_bp', __name__)

# /api/attributes
attributes_bp.route('/attributes', methods=['GET'])(attribute_controller.get_all_attributes_controller)
attributes_bp.route('/attributes', methods=['POST'])(attribute_controller.create_attribute_controller)

# /api/attributes/5
attributes_bp.route('/attributes/<int:attribute_id>', methods=['GET'])(attribute_controller.get_attribute_by_id_controller)
attributes_bp.route('/attributes/<int:attribute_id>', methods=['PUT'])(attribute_controller.update_attribute_controller)
attributes_bp.route('/attributes/<int:attribute_id>', methods=['DELETE'])(attribute_controller.delete_attribute_controller)