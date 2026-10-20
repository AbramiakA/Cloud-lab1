# --- my_project/service/review_service.py ---

from my_project.dao import review_dao

def get_all_reviews():
    """Отримує всі відгуки та конвертує їх у dict."""
    reviews = review_dao.find_all()
    return [review.to_dict() for review in reviews]

def get_review_by_id(review_id):
    """Отримує один відгук та конвертує його у dict."""
    review = review_dao.find_by_id(review_id)
    return review.to_dict() if review else None

def create_review(data):
    """Створює відгук та повертає його як dict."""
    new_id = review_dao.create(data)
    return get_review_by_id(new_id) if new_id else None

def update_review(review_id, data):
    """Оновлює відгук та повертає оновлену версію як dict."""
    rows_affected = review_dao.update(review_id, data)
    return get_review_by_id(review_id) if rows_affected > 0 else None

def delete_review(review_id):
    """Видаляє відгук. Повертає True (успішно) або False."""
    rows_affected = review_dao.delete(review_id)
    return rows_affected > 0