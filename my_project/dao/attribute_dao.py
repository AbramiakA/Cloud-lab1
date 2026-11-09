"""MySQL DAO for attributes; connections are always returned to the pool."""

from contextlib import closing

from my_project.database import get_db_connection
from my_project.domain.attribute import Attribute


BASE_SELECT = """
    SELECT * FROM attributes
"""


def find_all():
    """Return all attributes."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT)
            rows = cursor.fetchall()
    return [Attribute(**row) for row in rows]


def find_by_id(attribute_id):
    """Return attribute by ID or None when missing."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT + " WHERE attributes.id = %s", (attribute_id,))
            row = cursor.fetchone()
    return Attribute(**row) if row else None


def create(attribute_data):
    """Insert a attribute; return its new ID."""
    query = "INSERT INTO attributes (name) VALUES (%s)"
    values = (attribute_data.get("name"),)

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


def update(attribute_id, attribute_data):
    """Update allowed columns and return affected row count."""
    query = f"UPDATE attributes SET name = %s WHERE id = %s"
    values = (attribute_data.get("name"), attribute_id)

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


def delete(attribute_id):
    """Delete by ID and return affected row count."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute("DELETE FROM attributes WHERE id = %s", (attribute_id,))
                affected = cursor.rowcount
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    return affected
