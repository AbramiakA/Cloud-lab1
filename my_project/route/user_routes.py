from flask import Blueprint
from my_project.controller import user_controller

# Створюємо "креслення" (Blueprint) для маршрутів користувачів
users_bp = Blueprint('users_bp', __name__)

# З'єднуємо URL та методи (GET, POST, ...) з функціями контролера

users_bp.route('/users', methods=['GET'])(user_controller.get_all_users_controller)
users_bp.route('/users/<int:user_id>', methods=['GET'])(user_controller.get_user_by_id_controller)
users_bp.route('/users', methods=['POST'])(user_controller.create_user_controller)
users_bp.route('/users/<int:user_id>', methods=['PUT'])(user_controller.update_user_controller)
users_bp.route('/users/<int:user_id>', methods=['DELETE'])(user_controller.delete_user_controller)