from my_project.dao import user_dao

def get_all_users():
    """Отримує всіх користувачів та конвертує їх у dict."""
    users = user_dao.find_all_users()
    return [user.to_dict() for user in users]

def get_user_by_id(user_id):
    """Отримує одного користувача та конвертує його у dict."""
    user = user_dao.find_user_by_id(user_id)
    return user.to_dict() if user else None

def create_user(data):
    """Створює користувача та повертає його як dict."""
    # (Тут могла б бути валідація, напр. 'чи email унікальний?')
    new_id = user_dao.create_user(data)
    return get_user_by_id(new_id) if new_id else None

def update_user(user_id, data):
    """Оновлює користувача та повертає оновлену версію як dict."""
    rows_affected = user_dao.update_user(user_id, data)
    return get_user_by_id(user_id) if rows_affected > 0 else None

def delete_user(user_id):
    """Видаляє користувача. Повертає True (успішно) або False."""
    rows_affected = user_dao.delete_user(user_id)
    return rows_affected > 0