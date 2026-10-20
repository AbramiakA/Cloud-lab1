import os
import mysql.connector
from mysql.connector import pooling
from urllib.parse import urlparse

# Налаштування підключення до Бази Даних
database_url = os.getenv('DATABASE_URL')

if database_url:
    parsed_url = urlparse(database_url)

    db_config = {
        'host': parsed_url.hostname,
        'port': parsed_url.port or 3306,
        'user': parsed_url.username,
        'password': parsed_url.password,
        'database': parsed_url.path.lstrip('/')
    }
else:
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }

# Створюємо "Пул З'єднань" для ефективного використання
try:
    db_pool = pooling.MySQLConnectionPool(pool_name="my_pool",
                                          pool_size=5,
                                          **db_config)
    print("Пул з'єднань MySQL успішно створено!")
except mysql.connector.Error as err:
    print(f"Помилка при створенні пулу: {err}")
    exit()

def get_db_connection():
    """Бере одне вільне з'єднання з пулу."""
    try:
        conn = db_pool.get_connection()
        if conn.is_connected():
            return conn
    except mysql.connector.Error as err:
        print(f"Помилка при отриманні з'єднання: {err}")
        return None

def initialize_database():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_metadata (
                id INT PRIMARY KEY,
                initialized BOOLEAN NOT NULL
            )
        """)

        cursor.execute(
            "SELECT initialized FROM app_metadata WHERE id = 1"
        )

        row = cursor.fetchone()

        if row and row[0]:
            print("База даних вже ініціалізована.")
            return

        with open("init.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        statements = sql_script.split(";")

        for statement in statements:
            statement = statement.strip()

            if not statement:
                continue

            if statement.upper().startswith("CREATE SCHEMA"):
                continue

            if statement.upper().startswith("USE "):
                continue

            cursor.execute(statement)

        cursor.execute("""
            INSERT INTO app_metadata (id, initialized)
            VALUES (1, TRUE)
            ON DUPLICATE KEY UPDATE initialized = TRUE
        """)

        connection.commit()
        print("База даних успішно ініціалізована.")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()