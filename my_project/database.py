
import os
import mysql.connector
from sqlalchemy.pool import QueuePool
from urllib.parse import urlparse


# Налаштування підключення до бази даних
database_url = os.getenv("DATABASE_URL")

if database_url:
    parsed_url = urlparse(database_url)

    db_config = {
        "host": parsed_url.hostname,
        "port": parsed_url.port or 3306,
        "user": parsed_url.username,
        "password": parsed_url.password,
        "database": parsed_url.path.lstrip("/")
    }
else:
    db_config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME")
    }


# Динамічний пул з'єднань MySQL
db_pool = QueuePool(
    creator=lambda: mysql.connector.connect(**db_config),
    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
    max_overflow=int(os.getenv("DB_POOL_OVERFLOW", "5")),
    timeout=10,
    recycle=1800,
    reset_on_return="rollback"
)


def get_db_connection():
    """Отримує з'єднання з пулу, очікуючи за потреби."""
    return db_pool.connect()


def initialize_database():
    """Ініціалізує базу даних, якщо це ще не було зроблено."""
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()

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
        if cursor is not None:
            cursor.close()

        connection.close()
