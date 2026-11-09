"""MySQL DAO for subcategories; connections are always returned to the pool."""

from contextlib import closing

from my_project.database import get_db_connection
from my_project.domain.subcategory import Subcategory


BASE_SELECT = """
    SELECT s.*, c.name AS category_name
    FROM subcategories s
    LEFT JOIN categories c ON s.Categories_id = c.id
"""


def find_all():
    """Return all subcategories."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT)
            rows = cursor.fetchall()
    return [Subcategory(**row) for row in rows]


def find_by_id(subcategory_id):
    """Return subcategory by ID or None when missing."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT + " WHERE s.id = %s", (subcategory_id,))
            row = cursor.fetchone()
    return Subcategory(**row) if row else None


def create(data):
    """Insert a subcategory; return its new ID."""
    query = "INSERT INTO subcategories (name, Categories_id) VALUES (%s, %s)"
    values = (data.get("name"), data.get("Categories_id"),)

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


def update(subcategory_id, data):
    """Update allowed columns and return affected row count."""
    allowed = ['name', 'Categories_id']
    fields = [name for name in allowed if name in data]
    if not fields:
        return 0

    assignments = ", ".join(f"{name} = %s" for name in fields)
    query = f"UPDATE subcategories SET {assignments} WHERE id = %s"
    values = tuple(data[name] for name in fields) + (subcategory_id,)

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


def delete(subcategory_id):
    """Delete by ID and return affected row count."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute("DELETE FROM subcategories WHERE id = %s", (subcategory_id,))
                affected = cursor.rowcount
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    return affected
