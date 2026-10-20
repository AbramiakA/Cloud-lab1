import mysql.connector
from my_project.database import get_db_connection
from my_project.domain.user import User

def find_all_users():
    """Отримує всіх користувачів з БД."""
    conn = get_db_connection()
    if conn is None: return []

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [User(**row) for row in results]

def find_user_by_id(user_id):
    """Знаходить одного користувача за його ID."""
    conn = get_db_connection()
    if conn is None: return None

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return User(**result) if result else None

def create_user(user_data):
    """Створює нового користувача, повертає його new_id."""
    conn = get_db_connection()
    if conn is None: return None

    cursor = conn.cursor()
    query = """
    INSERT INTO users (full_name, email, password_hash, phone)
    VALUES (%s, %s, %s, %s)
    """
    data_tuple = (
        user_data.get('full_name'),
        user_data.get('email'),
        user_data.get('password_hash'),
        user_data.get('phone')
    )
    
    try:
        cursor.execute(query, data_tuple)
        conn.commit()
        new_id = cursor.lastrowid
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (create_user): {err}")
        return None
    finally:
        cursor.close()
        conn.close()
            
    return new_id

def update_user(user_id, user_data):
    """Оновлює користувача за ID. Повертає кількість змінених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    
    set_clauses = []
    data_values = []
    updatable_fields = ['full_name', 'email', 'password_hash', 'phone']
    
    for field in updatable_fields:
        if field in user_data:
            set_clauses.append(f"{field} = %s")
            data_values.append(user_data[field])

    if not set_clauses:
        cursor.close()
        conn.close()
        return 0

    set_statement = ", ".join(set_clauses)
    query = f"UPDATE users SET {set_statement} WHERE id = %s"
    data_values.append(user_id) 

    rows_affected = 0
    try:
        cursor.execute(query, tuple(data_values))
        conn.commit()
        rows_affected = cursor.rowcount
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (update_user): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected

def delete_user(user_id):
    """Видаляє користувача за ID. Повертає кількість видалених рядків (1 або 0)."""
    conn = get_db_connection()
    if conn is None: return 0

    cursor = conn.cursor()
    query = "DELETE FROM users WHERE id = %s"
    
    rows_affected = 0
    try:
        cursor.execute(query, (user_id,))
        conn.commit()
        rows_affected = cursor.rowcount 
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Помилка DAO (delete_user): {err}")
    finally:
        cursor.close()
        conn.close()
            
    return rows_affected