import asyncio
import logging
import re
import json
import sys
from typing import List, Mapping

import aiohttp
import aiosqlite
from bs4 import BeautifulSoup, element

import settings
from data.db_api import (db_add_product_into_suppliers,
                         select_one_where_and,
                         select_many_where_and,
                         update)
from misc.classes import Product
from misc.utils import fetch, write_to_excel
from misc.checkers import is_changes

logger = logging.getLogger(__name__)


async def make_all_products_data_dict(all_category_dict: dict, session: aiohttp.ClientSession):
    all_products_data_dict = {}
    await _make_all_products_data_dict(all_products_data_dict, all_category_dict, session)
    return all_products_data_dict


async def single_product_processing(product_from_site: Product, db: aiosqlite.Connection):
    product_from_db_suppliers = await get_product_from_db_suppliers(product_from_site, db)
    if product_from_db_suppliers is None:
        #! появился новый товар
        await db_add_product_into_suppliers(product_from_site, db)
        #! создать/дописать в файл new_today.xlsx
        #! оповещение
    else:
        if await is_changes(product_from_site, product_from_db_suppliers):
            #! изменился товар
            #! создать/дописать в файл change_today.xlsx
            print('is_changes')
            await update_product_in_db_suppliers(product_from_site, db)
            #! оповещение
    products_from_db_electrokom = await get_products_from_db_electrokom(product_from_site, db)
    if products_from_db_electrokom:
        product_from_db_electrokom: Product
        for product_from_db_electrokom in products_from_db_electrokom:
            if await is_changes(product_from_site, product_from_db_electrokom):
                await update_product_in_db_electrokom(product_from_site, db)
                await write_to_excel(
                    {
                        'Артикул': product_from_db_electrokom.sku,
                        'Цена': product_from_site.price if product_from_site.price > 0
                        else product_from_db_electrokom.price,
                        'Наличие': 'В наличии' if product_from_site.available
                        else 'Нет в наличии',
                    }
                )
    #         print(product.title)
    # sys.exit(1)
    # TODO проверить есть ли этот товар в бд электроком
    # TODO проверить легитимность изменение цены
    # product_from_db_electrokom = await get_products_from_db_electrokom
    # TODO если такой товар есть, то добавить его в csv-файл экспорта
    # TODO обновить этот товар в бд поставщик


async def worker(session, db, url, id_filter):
    product: Product
    # with open('soup.html', 'w') as file:
    #     file.write(await fetch(session, url))

    # with open('soup.html', 'r') as file:
    #     html = file.read()
    soup = BeautifulSoup(await fetch(session, url), 'lxml')
    # soup = BeautifulSoup(html, 'lxml')
    # # print('ok')
    total_pages = await _get_number_pages(soup)
    if total_pages == 0:
        logger.warning(
            f'{url} has no number_pages ({total_pages})')
    async for product in _get_all_products_on_page(soup, id_filter):
        await single_product_processing(product, db)
    for num_page in range(2, total_pages+1):
        async for product in _get_all_products_on_page(
                BeautifulSoup(await fetch(session, url+f'/page_{num_page}'), 'lxml'),
                id_filter):
            await single_product_processing(product, db)


async def _make_all_products_data_dict(all_products_data_dict: dict,
                                       all_category_dict: dict,
                                       session: aiohttp.ClientSession):
    id_filter = set()
    async with aiosqlite.connect('parser.db') as db:
        for key in range(len(all_category_dict), 0, -1):
            tasks = [asyncio.ensure_future(worker(session, db, url, id_filter))
                     for url in all_category_dict[str(key)].values()]

            #! for tests
            # tasks = [asyncio.ensure_future(
            #     worker(session,
            #            db,
            #            'https://turbovent.com.ua/ua/g7317438-osevye-promyshlennye-ventilyatory',
            #            id_filter
            #            )
            # )]

            await asyncio.gather(*tasks)
            # break


async def _get_all_products_on_page(soup: BeautifulSoup, id_filter: set) -> Product:
    item: element.ResultSet
    for item in soup.find_all('li', class_='b-product-gallery__item'):
        yield await _make_one_product_from_html(item, id_filter)


async def _make_one_product_from_html(item: element.ResultSet, id_filter: set) -> Product:
    id_website: str = await _get_product_id(item)
    if id_website is None and id_website in id_filter:
        return None
    id_filter.add(id_website)
    sku: str = await _get_product_sku(item, id_website)
    title: str = await _get_product_title(item, id_website)
    price: int = await _get_product_price(item, id_website)
    url: str = await _get_product_url(item, id_website)
    available: int = await _get_product_available(item, id_website)

    return Product(
        id_website=id_website,
        sku=sku,
        title=title,
        price=price,
        url=url,
        available=available,
    )


async def get_product_from_db_suppliers(product: Product,
                                        db: aiosqlite.Connection) -> Product:
    product_from_db_suppliers = await select_one_where_and('suppliers',
                                                           '*',
                                                           {'id_website': product.id_website},
                                                           db
                                                           )
    if product_from_db_suppliers is None:
        return None
    return Product(
        id_db=product_from_db_suppliers['id_db'],
        id_website=product_from_db_suppliers['id_website'],
        sku=product_from_db_suppliers['sku'],
        title=product_from_db_suppliers['title'],
        url=product_from_db_suppliers['url'],
        price=product_from_db_suppliers['price'],
        available=product_from_db_suppliers['available'],
    )


async def get_products_from_db_electrokom(product: Product,
                                          db: aiosqlite.Connection) -> List[Product]:
    products_from_db_electrokom = await select_many_where_and(
        'electrokom',
        '*',
        {'mnp': product.sku},
        db
    )
    if products_from_db_electrokom is None:
        return None
    products = []
    for _product in products_from_db_electrokom:
        products.append(
            Product(
                id_db=_product['id_db'],
                sku=_product['sku'],
                title=_product['title'],
                url=_product['url'],
                price=_product['price'],
                available=_product['available'],
                mnp=_product['mnp'],
            )
        )
    return products


async def update_product_in_db_suppliers(product: Product,
                                         db: aiosqlite.Connection):
    await update(
        'suppliers',
        {
            'price': product.price,
            'available': product.available
        },
        {
            'id_website': product.id_website
        },
        db
    )


async def update_product_in_db_electrokom(product: Product,
                                          db: aiosqlite.Connection):
    await update(
        'electrokom',
        {
            'price': product.price,
            'available': product.available
        },
        {
            'mnp': product.sku
        },
        db
    )


async def _get_number_pages(soup: BeautifulSoup) -> int:
    number_pages = soup.find('div', 'b-pager')
    if number_pages is None:
        return 0
    return int(number_pages.find('div').get('data-pagination-pages-count'))


async def _get_product_id(item: element.ResultSet) -> str:
    current_id = item.find('a', class_='b-online-edit__link')
    if current_id is None:
        return None
    return current_id.get('data-edit-id')


async def _get_product_sku(item: element.ResultSet, id: str) -> str:
    current_sku = item.find('span', class_='b-product-gallery__sku')
    if current_sku is None:
        logger.warning(f'{id} has no sku')
        return id
    return current_sku.text.strip()


async def _get_product_title(item: element.ResultSet, id: str) -> str:
    current_title = item.find('a', class_='b-goods-title')
    if current_title is None:
        logger.warning(f'{id} has no title')
        return 'no_title'
    return current_title.text.strip()


async def _get_product_price(item: element.ResultSet, id: str) -> int:
    price_text = item.find('span', class_='b-goods-price__value')
    regex = r"^[\s*\d*]+[\d+]+\s*₴\s*$"
    if price_text is None or re.match(regex, price_text.text) is None:
        logger.warning(f'{id} has no price')
        return 0
    return int(price_text.text.replace('\xa0', '').replace('₴', ''))


async def _get_product_url(item: element.ResultSet, id: str) -> str:
    current_url = item.find(
        'a', class_='b-goods-title')
    if current_url is None:
        logger.warning(f'{id} has no url')
        return 'no_url'
    return settings.domen + current_url.get('href').strip()


async def _get_product_available(item: element.ResultSet, id: str) -> int:
    current_available = item.find('span', class_='b-goods-data__state')
    if current_available is None:
        logger.warning(f'{id} has no available')
        return 0
    return settings.prom_available_dict.get(current_available.text.strip()) or 0
