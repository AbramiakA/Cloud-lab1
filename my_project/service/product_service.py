# --- my_project/service/product_service.py ---

from my_project.dao import product_dao

# Service = Логіка + перетворення "Об'єктів" (Domain) на "Словники" (dict/JSON)

def get_all_products():
    """
    Отримує всі товари, конвертує їх у dict,
    І ДЛЯ КОЖНОГО товару додає список його атрибутів.
    """
    
    # 1. Отримуємо базовий список товарів (вже з категоріями)
    products = product_dao.find_all_products()
    
    # 2. Конвертуємо їх у список словників (dict)
    product_list_as_dicts = [product.to_dict() for product in products]
    
    # 3. ⭐️ Ось нова "жадібна" логіка (цикл N+1) ⭐️
    for product_dict in product_list_as_dicts:
        # 4. Для кожного товару в списку ми робимо ДОДАТКОВИЙ запит в DAO
        product_id = product_dict['id']
        attributes = product_dao.find_attributes_for_product(product_id)
        
        # 5. Додаємо нове поле 'attributes' до словника
        product_dict['attributes'] = attributes
        
    # 6. Повертаємо повний, збагачений список
    return product_list_as_dicts

def get_product_by_id(product_id):
    """Отримує один товар та конвертує його у dict."""
    product = product_dao.find_product_by_id(product_id)
    return product.to_dict() if product else None

def create_product(data):
    """Створює товар та повертає його як dict."""
    # (Тут могла б бути валідація даних, напр. 'if data['price'] < 0')
    new_id = product_dao.create_product(data)
    return get_product_by_id(new_id) if new_id else None

def update_product(product_id, data):
    """Оновлює товар та повертає оновлену версію як dict."""
    rows_affected = product_dao.update_product(product_id, data)
    return get_product_by_id(product_id) if rows_affected > 0 else None

def delete_product(product_id):
    """Видаляє товар. Повертає True (успішно) або False."""
    rows_affected = product_dao.delete_product(product_id)
    return rows_affected > 0

def get_product_attributes(product_id):
    """
    Отримує список атрибутів для товару.
    DAO вже повертає дані у потрібному форматі (list[dict]).
    """
    attributes = product_dao.find_attributes_for_product(product_id)
    return attributes