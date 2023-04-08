import asyncio
import csv
import datetime
import logging
import os

import aiofiles
import aiosqlite
import pytz

from misc.classes import Product


logger = logging.getLogger(__name__)


async def db_create_tables() -> None:
    try:
        async with aiosqlite.connect('parser.db') as db:
            with open('data/init.sql', 'r') as f:
                sql = f.read()
            await db.executescript(sql)
            await db.commit()
    except Exception as err:
        logger.error(f'Error creating tables: {err}', exc_info=True)


async def db_add_product(tablename: str, product: Product, db: aiosqlite.Connection) -> None:
    await _insert(tablename,
                  {
                    'id_website': product.id,
                    'sku': product.sku,
                    'title': product.title,
                    'url': product.url,
                    'price': product.price,
                    'available': product.available
                  },
                  db)


async def _insert(tablename: str, column_values: dict, db: aiosqlite.Connection):
    columns = ', '.join(column_values.keys())
    values = tuple(column_values.values())
    placeholders = ', '.join('?' * len(column_values.keys()))
    try:
        await db.execute(
            f'INSERT INTO {tablename} '
            f'({columns}) '
            f'VALUES '
            f'({placeholders})',
            values
        )
        await db.commit()
        logger.info(
            f'inserting "{values[0]}" into a "{tablename}"'
        )
    except Exception as err:
        logger.error(f'Error inserting into "{tablename}": {err}', exc_info=True)


async def get_product_from_db(tablename: str, product_id: dict, db: aiosqlite.Connection) -> bool:
    column = ''.join(product_id.keys())
    value = ''.join(product_id.values())
    sql = f"SELECT * FROM {tablename} WHERE {column} = ?"
    try:
        async with db.execute(sql, (value,)) as cursor:
            row = await cursor.fetchone()
            return row or None
    except Exception as err:
        logger.error(f'Error checking product in database: {err}', exc_info=True)
        return False


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     a1 = loop.create_task(main())
#     loop.run_until_complete(a1)
