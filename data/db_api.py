import asyncio
import csv
import datetime
import logging
import os
import sys
from typing import Dict, List, Mapping
import settings

import aiofiles
import aiosqlite
import pytz

from misc.classes import AlreadyBeenCreated, Product


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


async def db_add_product_into_suppliers(product: Product, db: aiosqlite.Connection) -> None:
    await _insert('suppliers',
                  {
                      'id_website': product.id_website,
                      'sku': product.sku,
                      'title': product.title,
                      'url': product.url,
                      'price': product.price,
                      'available': product.available
                  },
                  db
                  )


async def db_add_product_into_electrokom_from_excel(entry: Dict, db: aiosqlite.Connection) -> None:
    if isinstance(entry.get('mnp'), str):
        try:
            await _insert('electrokom',
                          {
                              'sku': str(entry.get('sku')),
                              'title': entry.get('title'),
                              'url': entry.get('url'),
                              'price': int(entry.get('price')),
                              'available': int(settings.electrokom_available_dict.get(
                                  entry.get('available'))),
                              'mnp': entry.get('mnp'),
                          },
                          db
                          )
        except AlreadyBeenCreated:
            logger.warning(
                f'{entry.get("title")} already created, needs to be updated')
    else:
        print(f'{entry.get("title")} dont have mnp')


async def select_one_where_and(tablename: str,
                               columns: List[str],
                               definitions: Mapping[str, str],
                               db: aiosqlite.Connection) -> aiosqlite.Row:
    columns_joined = ', '.join(columns)
    definition_joined_placeholders = ' AND '.join(
        [f'{field}=?' for field in definitions.keys()])
    values = tuple(definitions.values())
    sql = (
        f"SELECT {columns_joined} "
        f"FROM {tablename} "
        f"WHERE {definition_joined_placeholders}"
    )
    db.row_factory = aiosqlite.Row
    try:
        async with db.execute(sql, values) as cursor:
            row = await cursor.fetchone()
            return row or None
    except Exception as err:
        logger.error(
            f'Error checking product in database: {err}', exc_info=True)
        return False


async def select_many_where_and(tablename: str,
                                columns: List[str],
                                definitions: Mapping[str, str],
                                db: aiosqlite.Connection) -> aiosqlite.Row:
    columns_joined = ', '.join(columns)
    definition_joined_placeholders = ' AND '.join(
        [f'{field}=?' for field in definitions.keys()])
    values = tuple(definitions.values())
    sql = (
        f"SELECT {columns_joined} "
        f"FROM {tablename} "
        f"WHERE {definition_joined_placeholders}"
    )
    db.row_factory = aiosqlite.Row
    try:
        async with db.execute_fetchall(sql, values) as rows:
            return rows or None
    except Exception as err:
        logger.error(
            f'Error checking product in database: {err}', exc_info=True)
        return None


async def _insert(tablename: str, column_values: Dict, db: aiosqlite.Connection):
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
    except aiosqlite.IntegrityError:
        raise AlreadyBeenCreated
    except Exception as err:
        logger.error(
            f'Error inserting into "{tablename}": {err}', exc_info=True)


async def update(tablename: str,
                  column_values: Dict,
                  definitions: Mapping[str, str],
                  db: aiosqlite.Connection):
    '''
    update electrokom set price=1, available=0 where mnp='SIGMA200'
    'price': 1, 'available': 0,
    'mnp': 'SIGMA200'
    '''
    set_ = ', '.join([f'{column}=?' for column in column_values.keys()])
    definition_joined_placeholders = ' AND '.join(
        [f'{field}=?' for field in definitions.keys()])
    values = tuple(list(column_values.values()) + list(definitions.values()))
    sql = (
        f'UPDATE {tablename} '
        f'SET {set_} '
        f'WHERE {definition_joined_placeholders}'
    )
    try:
        await db.execute(sql,values)
        await db.commit()
        logger.info(
            f'update "{values[-1]}" into a "{tablename}"'
        )
    except Exception as err:
        logger.error(
            f'Error inserting into "{tablename}": {err}', exc_info=True)


# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     a1 = loop.create_task(main())
#     loop.run_until_complete(a1)
