from typing import NamedTuple

class Product(NamedTuple):
    id_db: int = None
    id_website: str = None
    sku: str = None
    title: str = None
    price: int = None
    url: str = None
    available: int = None
    mnp: str | None = None


class Too_Many_Requests(Exception): pass
class AlreadyBeenCreated(Exception): pass
