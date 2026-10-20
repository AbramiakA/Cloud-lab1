import mysql.connector
from my_project.database import get_db_connection
from my_project.domain.attribute import Attribute

def find_all():
    """Отримує всі атрибути з БД."""
    conn = get_db_connection()
    if conn is None: return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attributes")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [Attribute(**row) for row in results]

def find_by_id(attribute_id):
    """Знаходить один атрибут за його ID."""
    conn = get_db_connection()
    if conn is None: return None
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attributes WHERE id = %s", (attribute_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return Attribute(**result) if result else None

def create(attribute_data):
    """Створює новий атрибут, повертає його new_id."""
    conn = get_db_connection()
    if conn is None: return None

    cursor = conn.cursor()
    query = "INSERT INTO attributes (name) VALUES (%s)"
    
    try:
        cursor.execute(query, (attribute_data.get('name'),))
        conn.commit()
        new_id = cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (create_attribute): {err}")
        return None
    finally:
        cursor.close()
        conn.close()
            
    return new_id

def update(attribute_id, attribute_data):
    """Оновлює атрибут за ID. Повертає кількість змінених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    query = "UPDATE attributes SET name = %s WHERE id = %s"
    data_tuple = (attribute_data.get('name'), attribute_id)

    rows_affected = 0
    try:
        cursor.execute(query, data_tuple)
        conn.commit()
        rows_affected = cursor.rowcount
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (update_attribute): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected

def delete(attribute_id):
    """Видаляє атрибут за ID. Повертає кількість видалених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    query = "DELETE FROM attributes WHERE id = %s"
    
    rows_affected = 0
    try:
        cursor.execute(query, (attribute_id,))
        conn.commit()
        rows_affected = cursor.rowcount 
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (delete_attribute): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected