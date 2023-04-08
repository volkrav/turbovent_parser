from misc.classes import Product


async def check_product(product: Product, product_from_db):
    pass
    if product.price != product_from_db[5] or product.available != product_from_db[-1]:
        print('no equale')
        # TODO проверить есть ли этот товар в бд электроком
            # TODO если такой товар есть, то добавить его в csv-файл экспорта
        # TODO обновить этот товар в бд поставщик
    else:
        print("ok")
