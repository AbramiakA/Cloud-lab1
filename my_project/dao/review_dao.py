"""MySQL DAO for reviews; connections are always returned to the pool."""

from contextlib import closing

from my_project.database import get_db_connection
from my_project.domain.review import Review


BASE_SELECT = """
    SELECT * FROM reviews
"""


def find_all():
    """Return all reviews."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT)
            rows = cursor.fetchall()
    return [Review(**row) for row in rows]


def find_by_id(review_id):
    """Return review by ID or None when missing."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(BASE_SELECT + " WHERE reviews.id = %s", (review_id,))
            row = cursor.fetchone()
    return Review(**row) if row else None


def create(data):
    """Insert a review; return its new ID."""
    query = "INSERT INTO reviews (rating, comment, Users_id, Products_id) VALUES (%s, %s, %s, %s)"
    values = (data.get("rating"), data.get("comment"), data.get("Users_id"), data.get("Products_id"),)

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


def update(review_id, data):
    """Update allowed columns and return affected row count."""
    allowed = ['rating', 'comment']
    fields = [name for name in allowed if name in data]
    if not fields:
        return 0

    assignments = ", ".join(f"{name} = %s" for name in fields)
    query = f"UPDATE reviews SET {assignments} WHERE id = %s"
    values = tuple(data[name] for name in fields) + (review_id,)

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


def delete(review_id):
    """Delete by ID and return affected row count."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
                affected = cursor.rowcount
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    return affected
