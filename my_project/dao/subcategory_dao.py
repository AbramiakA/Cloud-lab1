# --- my_project/dao/subcategory_dao.py ---

import mysql.connector
from my_project.database import get_db_connection
from my_project.domain.subcategory import Subcategory
from my_project.domain.category import Category

def find_all():
    """Отримує всі підкатегорії з БД разом з їхніми категоріями."""
    conn = get_db_connection()
    if conn is None: return []

    cursor = conn.cursor(dictionary=True)
    # ЗМІНЕНИЙ ЗАПИТ З JOIN
    query = """
    SELECT 
        s.*, 
        c.name AS category_name 
    FROM 
        subcategories s
    LEFT JOIN 
        categories c ON s.Categories_id = c.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [Subcategory(**row) for row in results]

def find_by_id(subcategory_id):
    """Знаходить одну підкатегорію за її ID разом з її категорією."""
    conn = get_db_connection()
    if conn is None: return None
        
    cursor = conn.cursor(dictionary=True)
    # ЗМІНЕНИЙ ЗАПИТ З JOIN
    query = """
    SELECT 
        s.*, 
        c.name AS category_name 
    FROM 
        subcategories s
    LEFT JOIN 
        categories c ON s.Categories_id = c.id
    WHERE 
        s.id = %s
    """
    
    cursor.execute(query, (subcategory_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return Subcategory(**result) if result else None

def create(data):
    """Створює нову підкатегорію, повертає її new_id."""
    conn = get_db_connection()
    if conn is None: return None

    cursor = conn.cursor()
    query = "INSERT INTO subcategories (name, Categories_id) VALUES (%s, %s)"
    data_tuple = (
        data.get('name'),
        data.get('Categories_id') # Додано поле зв'язку
    )
    
    try:
        cursor.execute(query, data_tuple)
        conn.commit()
        new_id = cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (create_subcategory): {err}")
        return None
    finally:
        cursor.close()
        conn.close()
            
    return new_id

def update(subcategory_id, data):
    """Оновлює підкатегорію за ID. Повертає кількість змінених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    
    # Динамічне оновлення, оскільки можна змінити або 'name', або 'Categories_id'
    set_clauses = []
    data_values = []
    
    if 'name' in data:
        set_clauses.append("name = %s")
        data_values.append(data['name'])
        
    if 'Categories_id' in data:
        set_clauses.append("Categories_id = %s")
        data_values.append(data['Categories_id'])

    if not set_clauses: # Нічого оновлювати
        cursor.close()
        conn.close()
        return 0

    set_statement = ", ".join(set_clauses)
    query = f"UPDATE subcategories SET {set_statement} WHERE id = %s"
    data_values.append(subcategory_id) 

    rows_affected = 0
    try:
        cursor.execute(query, tuple(data_values))
        conn.commit()
        rows_affected = cursor.rowcount
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (update_subcategory): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected

def delete(subcategory_id):
    """Видаляє підкатегорію за ID. Повертає кількість видалених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    query = "DELETE FROM subcategories WHERE id = %s"
    
    rows_affected = 0
    try:
        cursor.execute(query, (subcategory_id,))
        conn.commit()
        rows_affected = cursor.rowcount 
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (delete_subcategory): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected