# --- my_project/dao/product_dao.py ---

import mysql.connector
from my_project.database import get_db_connection
from my_project.domain.product import Product
from my_project.domain.subcategory import Subcategory # <-- Переконайся, що цей імпорт є

def find_all_products():
    """Отримує всі товари з БД разом з даними про підкатегорії І категорії."""
    conn = get_db_connection()
    if conn is None: return []

    cursor = conn.cursor(dictionary=True)
    
    # --- ОНОВЛЕНИЙ ЗАПИТ (DOUBLE JOIN) ---
    query = """
    SELECT 
        p.*, 
        s.name AS subcategory_name,
        s.Categories_id, 
        c.name AS category_name
    FROM 
        products p
    LEFT JOIN 
        subcategories s ON p.Subcategories_id = s.id
    LEFT JOIN
        categories c ON s.Categories_id = c.id
    """
    # --- КІНЕЦЬ ОНОВЛЕННЯ ---

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Конвертуємо list[dict] у list[Product]
    # Це спрацює, бо наш Product.__init__ тепер приймає нові поля
    return [Product(**row) for row in results]

def find_product_by_id(product_id):
    """Знаходить один товар за ID разом з даними про підкатегорію І категорію."""
    conn = get_db_connection()
    if conn is None: return None
        
    cursor = conn.cursor(dictionary=True)
    
    # --- ОНОВЛЕНИЙ ЗАПИТ (DOUBLE JOIN) ---
    query = """
    SELECT 
        p.*, 
        s.name AS subcategory_name,
        s.Categories_id, 
        c.name AS category_name
    FROM 
        products p
    LEFT JOIN 
        subcategories s ON p.Subcategories_id = s.id
    LEFT JOIN
        categories c ON s.Categories_id = c.id
    WHERE 
        p.id = %s
    """
    # --- КІНЕЦЬ ОНОВЛЕННЯ ---
    
    cursor.execute(query, (product_id,))
    result = cursor.fetchone() 
    cursor.close()
    conn.close()
    
    return Product(**result) if result else None

# --- ФУНКЦІЇ НИЖЧЕ ЗАЛИШАЮТЬСЯ БЕЗ ЗМІН ---

def create_product(product_data):
    """Створює новий товар, повертає його new_id."""
    conn = get_db_connection()
    if conn is None: return None

    cursor = conn.cursor()
    query = """
    INSERT INTO products (name, description, price, stock_quantity, Subcategories_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    data_tuple = (
        product_data.get('name'),
        product_data.get('description'),
        product_data.get('price'),
        product_data.get('stock_quantity'),
        product_data.get('Subcategories_id')
    )
    
    try:
        cursor.execute(query, data_tuple)
        conn.commit()
        new_id = cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback() 
        print(f"Помилка DAO (create_product): {err}")
        return None
    finally:
        cursor.close()
        conn.close()
            
    return new_id

def update_product(product_id, product_data):
    """Оновлює товар за ID. Повертає кількість змінених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    
    set_clauses = []
    data_values = []
    updatable_fields = ['name', 'description', 'price', 'stock_quantity', 'Subcategories_id']
    
    for field in updatable_fields:
        if field in product_data:
            set_clauses.append(f"{field} = %s")
            data_values.append(product_data[field])

    if not set_clauses: 
        cursor.close()
        conn.close()
        return 0

    set_statement = ", ".join(set_clauses)
    query = f"UPDATE products SET {set_statement} WHERE id = %s"
    data_values.append(product_id) 

    rows_affected = 0
    try:
        cursor.execute(query, tuple(data_values))
        conn.commit()
        rows_affected = cursor.rowcount 
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (update_product): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected

def delete_product(product_id):
    """Видаляє товар за ID. Повертає кількість видалених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    query = "DELETE FROM products WHERE id = %s"
    
    rows_affected = 0
    try:
        cursor.execute(query, (product_id,))
        conn.commit()
        rows_affected = cursor.rowcount 
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (delete_product): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected

def find_attributes_for_product(product_id):
    """
    Знаходить усі атрибути (назва + значення) для конкретного товару.
    Це запит для зв'язку M:M.
    """
    conn = get_db_connection()
    if conn is None: return []

    cursor = conn.cursor(dictionary=True)
    
    # --- ГОЛОВНИЙ ЗАПИТ M:M (JOIN ЧЕРЕЗ 3 ТАБЛИЦІ) ---
    query = """
    SELECT 
        a.name, 
        pha.value
    FROM 
        products_has_attributes pha
    JOIN 
        attributes a ON pha.Attributes_id = a.id
    WHERE 
        pha.Products_id = %s
    """
    # --- КІНЕЦЬ ЗАПИТУ ---

    cursor.execute(query, (product_id,))
    results = cursor.fetchall() # Поверне list[dict], напр. [{'name': 'Колір', 'value': 'Чорний'}, ...]
    cursor.close()
    conn.close()
    
    return results
