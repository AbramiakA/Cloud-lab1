# --- my_project/service/subcategory_service.py ---

from my_project.dao import subcategory_dao

def get_all_subcategories():
    """Отримує всі підкатегорії та конвертує їх у dict."""
    subcategories = subcategory_dao.find_all()
    return [subcategory.to_dict() for subcategory in subcategories]

def get_subcategory_by_id(subcategory_id):
    """Отримує одну підкатегорію та конвертує її у dict."""
    subcategory = subcategory_dao.find_by_id(subcategory_id)
    return subcategory.to_dict() if subcategory else None

def create_subcategory(data):
    """Створює підкатегорію та повертає її як dict."""
    new_id = subcategory_dao.create(data)
    return get_subcategory_by_id(new_id) if new_id else None

def update_subcategory(subcategory_id, data):
    """Оновлює підкатегорію та повертає оновлену версію як dict."""
    rows_affected = subcategory_dao.update(subcategory_id, data)
    return get_subcategory_by_id(subcategory_id) if rows_affected > 0 else None

def delete_subcategory(subcategory_id):
    """Видаляє підкатегорію. Повертає True (успішно) або False."""
    rows_affected = subcategory_dao.delete(subcategory_id)
    return rows_affected > 0