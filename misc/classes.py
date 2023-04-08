from typing import NamedTuple

class Product(NamedTuple):
    id: str
    sku: str
    title: str
    price: int
    url: str
    available: int
    mnp: str = None


class Too_Many_Requests(Exception): pass
