"""MySQL DAO for users; connections are always returned to the pool."""

from contextlib import closing

from my_project.database import get_db_connection
from my_project.domain.user import User


BASE_SELECT = """
    SELECT * FROM users
"""


def find_all_users():
    """Return all users."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT)
            rows = cursor.fetchall()
    return [User(**row) for row in rows]


def find_user_by_id(user_id):
    """Return user by ID or None when missing."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT + " WHERE users.id = %s", (user_id,))
            row = cursor.fetchone()
    return User(**row) if row else None


def create_user(user_data):
    """Insert a user; return its new ID."""
    query = "INSERT INTO users (full_name, email, password_hash, phone) VALUES (%s, %s, %s, %s)"
    values = (user_data.get("full_name"), user_data.get("email"), user_data.get("password_hash"), user_data.get("phone"),)

    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute(query, values)
                new_id = cursor.lastrowid
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    return new_id


def update_user(user_id, user_data):
    """Update allowed columns and return affected row count."""
    allowed = ['full_name', 'email', 'password_hash', 'phone']
    fields = [name for name in allowed if name in user_data]
    if not fields:
        return 0

    assignments = ", ".join(f"{name} = %s" for name in fields)
    query = f"UPDATE users SET {assignments} WHERE id = %s"
    values = tuple(user_data[name] for name in fields) + (user_id,)

    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute(query, values)
                affected = cursor.rowcount
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    return affected


def delete_user(user_id):
    """Delete by ID and return affected row count."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                affected = cursor.rowcount
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    return affected
