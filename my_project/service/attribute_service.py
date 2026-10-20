from my_project.dao import attribute_dao

def get_all_attributes():
    """Отримує всі атрибути та конвертує їх у dict."""
    attributes = attribute_dao.find_all()
    return [attribute.to_dict() for attribute in attributes]

def get_attribute_by_id(attribute_id):
    """Отримує один атрибут та конвертує його у dict."""
    attribute = attribute_dao.find_by_id(attribute_id)
    return attribute.to_dict() if attribute else None

def create_attribute(data):
    """Створює атрибут та повертає його як dict."""
    new_id = attribute_dao.create(data)
    return get_attribute_by_id(new_id) if new_id else None

def update_attribute(attribute_id, data):
    """Оновлює атрибут та повертає оновлену версію як dict."""
    rows_affected = attribute_dao.update(attribute_id, data)
    return get_attribute_by_id(attribute_id) if rows_affected > 0 else None

def delete_attribute(attribute_id):
    """Видаляє атрибут. Повертає True (успішно) або False."""
    rows_affected = attribute_dao.delete(attribute_id)
    return rows_affected > 0