# --- my_project/dao/review_dao.py ---

import mysql.connector
from my_project.database import get_db_connection
from my_project.domain.review import Review

def find_all():
    """Отримує всі відгуки з БД."""
    conn = get_db_connection()
    if conn is None: return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reviews")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [Review(**row) for row in results]

def find_by_id(review_id):
    """Знаходить один відгук за його ID."""
    conn = get_db_connection()
    if conn is None: return None
        
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reviews WHERE id = %s", (review_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return Review(**result) if result else None

def create(data):
    """Створює новий відгук, повертає його new_id."""
    conn = get_db_connection()
    if conn is None: return None

    cursor = conn.cursor()
    # `created_at` встановлюється автоматично (DEFAULT CURRENT_TIMESTAMP)
    query = """
    INSERT INTO reviews (rating, comment, Users_id, Products_id) 
    VALUES (%s, %s, %s, %s)
    """
    data_tuple = (
        data.get('rating'),
        data.get('comment'),
        data.get('Users_id'),
        data.get('Products_id')
    )
    
    try:
        cursor.execute(query, data_tuple)
        conn.commit()
        new_id = cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (create_review): {err}")
        return None
    finally:
        cursor.close()
        conn.close()
            
    return new_id

def update(review_id, data):
    """Оновлює відгук за ID. (Дозволяємо міняти 'rating' і 'comment')."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    
    set_clauses = []
    data_values = []
    
    if 'rating' in data:
        set_clauses.append("rating = %s")
        data_values.append(data['rating'])
        
    if 'comment' in data:
        set_clauses.append("comment = %s")
        data_values.append(data['comment'])

    if not set_clauses: # Нічого оновлювати
        cursor.close()
        conn.close()
        return 0

    set_statement = ", ".join(set_clauses)
    query = f"UPDATE reviews SET {set_statement} WHERE id = %s"
    data_values.append(review_id) 

    rows_affected = 0
    try:
        cursor.execute(query, tuple(data_values))
        conn.commit()
        rows_affected = cursor.rowcount
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (update_review): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected

def delete(review_id):
    """Видаляє відгук за ID. Повертає кількість видалених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    query = "DELETE FROM reviews WHERE id = %s"
    
    rows_affected = 0
    try:
        cursor.execute(query, (review_id,))
        conn.commit()
        rows_affected = cursor.rowcount 
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (delete_review): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected