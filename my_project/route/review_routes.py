# --- my_project/route/review_routes.py ---

from flask import Blueprint
from my_project.controller import review_controller

reviews_bp = Blueprint('reviews_bp', __name__)

# /api/reviews
reviews_bp.route('/reviews', methods=['GET'])(review_controller.get_all_reviews_controller)
reviews_bp.route('/reviews', methods=['POST'])(review_controller.create_review_controller)

# /api/reviews/5
reviews_bp.route('/reviews/<int:review_id>', methods=['GET'])(review_controller.get_review_by_id_controller)
reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])(review_controller.update_review_controller)
reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])(review_controller.delete_review_controller)