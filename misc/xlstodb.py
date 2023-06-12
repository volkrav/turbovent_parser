import asyncio
import logging
from typing import Dict, Generator, NamedTuple

import aiosqlite
import pandas as pd

from data.db_api import db_add_product_into_electrokom_from_excel

logger = logging.getLogger(__name__)


electrokom_available_dict = {
    'В наявності': 1,
    'Немає в наявності': 0,
    'Очікується': 0,
    'Статус не выбран': 0
}


async def process_excel(filename: str) -> Generator:
    # список заголовков, которые нужно обработать
    columns_to_include = {
        'sku': 'Артикул',
        'title': 'Название (UA)',
        'url': 'Ссылка',
        'price': 'Цена',
        'available': 'Наличие',
        'mnp': 'Код производителя товара (MPN)',
    }
    # чтение данных из файла excel
    df = pd.read_excel(filename)

    # создание списка словарей с нужными данными
    for _, row in df.iterrows():
        entry = {}
        for field_name, column_name in columns_to_include.items():
            entry[field_name] = row[column_name]
        yield entry


async def db_insert_electrokom_from_xls(path):
    async with aiosqlite.connect('parser.db') as db:
        row_gen_pd = process_excel(path)
        async for item in row_gen_pd:
            await db_add_product_into_electrokom_from_excel(item, db)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    a1 = loop.create_task(db_insert_electrokom_from_xls(
        '/Users/volodymyr/Projects/turbovent_parser/inbox/example_xls_to_db.xlsx'
    ))
    loop.run_until_complete(a1)
