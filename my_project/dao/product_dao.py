"""SQL operations for products. Connections are returned to the pool."""

from contextlib import closing

from my_project.database import get_db_connection
from my_project.domain.product import Product


PRODUCT_SELECT = """
    SELECT
        p.*,
        s.name AS subcategory_name,
        s.Categories_id,
        c.name AS category_name
    FROM products p
    LEFT JOIN subcategories s ON p.Subcategories_id = s.id
    LEFT JOIN categories c ON s.Categories_id = c.id
"""


def find_all_products(limit=20, offset=0):
    """Read one page of products, including category details."""
    query = PRODUCT_SELECT + " ORDER BY p.id LIMIT %s OFFSET %s"

    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(query, (limit, offset))
            rows = cursor.fetchall()

    return [Product(**row) for row in rows]


def find_attributes_for_products(product_ids):
    """Fetch attributes for a page of products in one SQL query."""
    if not product_ids:
        return {}

    placeholders = ", ".join(["%s"] * len(product_ids))
    query = f"""
        SELECT
            pha.Products_id AS product_id,
            a.name,
            pha.value
        FROM products_has_attributes pha
        JOIN attributes a ON pha.Attributes_id = a.id
        WHERE pha.Products_id IN ({placeholders})
        ORDER BY pha.Products_id, a.id
    """

    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(query, tuple(product_ids))
            rows = cursor.fetchall()

    attributes_by_product = {product_id: [] for product_id in product_ids}
    for row in rows:
        attributes_by_product[row["product_id"]].append({
            "name": row["name"],
            "value": row["value"]
        })

    return attributes_by_product


def find_product_by_id(product_id):
    """Read one product, including category details."""
    query = PRODUCT_SELECT + " WHERE p.id = %s"

    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()

    return Product(**row) if row else None


def create_product(product_data):
    """Create and return a product using one DB connection and transaction."""
    insert_query = """
        INSERT INTO products
            (name, description, price, stock_quantity, Subcategories_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        product_data.get("name"),
        product_data.get("description"),
        product_data.get("price"),
        product_data.get("stock_quantity"),
        product_data.get("Subcategories_id")
    )

    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            try:
                cursor.execute(insert_query, values)
                new_id = cursor.lastrowid
                cursor.execute(PRODUCT_SELECT + " WHERE p.id = %s", (new_id,))
                row = cursor.fetchone()
                if row is None:
                    raise RuntimeError("Created product could not be read")
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    return Product(**row)


def update_product(product_id, product_data):
    """Update allowed fields; return the number of changed rows."""
    allowed_fields = [
        "name", "description", "price", "stock_quantity", "Subcategories_id"
    ]
    fields = [field for field in allowed_fields if field in product_data]
    if not fields:
        return 0

    assignments = ", ".join(f"{field} = %s" for field in fields)
    query = f"UPDATE products SET {assignments} WHERE id = %s"
    values = tuple(product_data[field] for field in fields) + (product_id,)

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


def delete_product(product_id):
    """Delete a product; return the number of deleted rows."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            try:
                cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
                affected = cursor.rowcount
                conn.commit()
            except Exception:
                conn.rollback()
                raise

    return affected


def find_attributes_for_product(product_id):
    """Read attributes for a single product."""
    query = """
        SELECT a.name, pha.value
        FROM products_has_attributes pha
        JOIN attributes a ON pha.Attributes_id = a.id
        WHERE pha.Products_id = %s
    """

    with closing(get_db_connection()) as conn:
        with closing(conn.cursor(dictionary=True)) as cursor:
            cursor.execute(query, (product_id,))
            rows = cursor.fetchall()

    return rows
