import mysql.connector
from my_project.database import get_db_connection
from my_project.domain.category import Category

def find_all():
    """Отримує всі категорії з БД."""
    conn = get_db_connection()
    if conn is None: return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [Category(**row) for row in results]

def find_by_id(category_id):
    """Знаходить одну категорію за її ID."""
    conn = get_db_connection()
    if conn is None: return None
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return Category(**result) if result else None

def create(category_data):
    """Створює нову категорію, повертає її new_id."""
    conn = get_db_connection()
    if conn is None: return None

    cursor = conn.cursor()
    query = "INSERT INTO categories (name) VALUES (%s)"
    
    try:
        cursor.execute(query, (category_data.get('name'),))
        conn.commit()
        new_id = cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (create_category): {err}")
        return None
    finally:
        cursor.close()
        conn.close()
            
    return new_id

def update(category_id, category_data):
    """Оновлює категорію за ID. Повертає кількість змінених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    query = "UPDATE categories SET name = %s WHERE id = %s"
    data_tuple = (category_data.get('name'), category_id)

    rows_affected = 0
    try:
        cursor.execute(query, data_tuple)
        conn.commit()
        rows_affected = cursor.rowcount
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (update_category): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected

def delete(category_id):
    """Видаляє категорію за ID. Повертає кількість видалених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    query = "DELETE FROM categories WHERE id = %s"
    
    rows_affected = 0
    try:
        cursor.execute(query, (category_id,))
        conn.commit()
        rows_affected = cursor.rowcount 
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (delete_category): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected