import sys
from misc.classes import Product


async def is_changes(product: Product, product_from_db_suppliers: Product):
    pass
    return product.price != product_from_db_suppliers.price or\
            product.available != product_from_db_suppliers.available
