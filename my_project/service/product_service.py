from my_project.dao import product_dao
from my_project.service import product_cache


def get_all_products(page=1, limit=20):
    """Return a paginated product list with attributes (no N+1 queries)."""
    offset = (page - 1) * limit
    products = product_dao.find_all_products(limit=limit, offset=offset)
    attributes_by_id = product_dao.find_attributes_for_products(
        [product.id for product in products]
    )

    result = []
    for product in products:
        product_dict = product.to_dict()
        product_dict["attributes"] = attributes_by_id.get(product.id, [])
        result.append(product_dict)

    return result


def get_product_by_id(product_id):
    product = product_dao.find_product_by_id(product_id)
    return product.to_dict() if product else None

def get_cached_product_by_id(product_id):
    return product_cache.get_or_load(
        product_id,
        lambda: get_product_by_id(product_id)
    )

def create_product(data):
    product = product_dao.create_product(data)
    return product.to_dict()


def update_product(product_id, data):
    changed = product_dao.update_product(product_id, data)

    if changed <= 0:
        return None

    product_cache.invalidate(product_id)
    return get_product_by_id(product_id)


def delete_product(product_id):
    deleted = product_dao.delete_product(product_id) > 0

    if deleted:
        product_cache.invalidate(product_id)

    return deleted


def get_product_attributes(product_id):
    return product_dao.find_attributes_for_product(product_id)
