from my_project.dao import category_dao

def get_all_categories():
    """Отримує всі категорії та конвертує їх у dict."""
    categories = category_dao.find_all()
    return [category.to_dict() for category in categories]

def get_category_by_id(category_id):
    """Отримує одну категорію та конвертує її у dict."""
    category = category_dao.find_by_id(category_id)
    return category.to_dict() if category else None

def create_category(data):
    """Створює категорію та повертає її як dict."""
    new_id = category_dao.create(data)
    return get_category_by_id(new_id) if new_id else None

def update_category(category_id, data):
    """Оновлює категорію та повертає оновлену версію як dict."""
    rows_affected = category_dao.update(category_id, data)
    return get_category_by_id(category_id) if rows_affected > 0 else None

def delete_category(category_id):
    """Видаляє категорію. Повертає True (успішно) або False."""
    rows_affected = category_dao.delete(category_id)
    return rows_affected > 0