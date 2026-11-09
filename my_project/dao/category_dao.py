"""MySQL DAO for categories; connections are always returned to the pool."""

from contextlib import closing

from my_project.database import get_db_connection
from my_project.domain.category import Category


BASE_SELECT = """
    SELECT * FROM categories
"""


def find_all():
    """Return all categories."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT)
            rows = cursor.fetchall()
    return [Category(**row) for row in rows]


def find_by_id(category_id):
    """Return category by ID or None when missing."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT + " WHERE categories.id = %s", (category_id,))
            row = cursor.fetchone()
    return Category(**row) if row else None


def create(category_data):
    """Insert a category; return its new ID."""
    query = "INSERT INTO categories (name) VALUES (%s)"
    values = (category_data.get("name"),)

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


def update(category_id, category_data):
    """Update allowed columns and return affected row count."""
    query = f"UPDATE categories SET name = %s WHERE id = %s"
    values = (category_data.get("name"), category_id)

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


def delete(category_id):
    """Delete by ID and return affected row count."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
                affected = cursor.rowcount
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    return affected
