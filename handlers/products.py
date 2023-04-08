import logging
import re
import json

import aiohttp
import aiosqlite
from bs4 import BeautifulSoup, element

import settings
from data.db_api import get_product_from_db, db_add_product
from misc.classes import Product
from misc.utils import fetch
from misc.checkers import check_product

logger = logging.getLogger(__name__)


async def make_all_products_data_dict(all_category_dict: dict, session: aiohttp.ClientSession):
    all_products_data_dict = {}
    await _make_all_products_data_dict(all_products_data_dict, all_category_dict, session)
    return all_products_data_dict


async def _make_all_products_data_dict(all_products_data_dict: dict,
                                       all_category_dict: dict,
                                       session: aiohttp.ClientSession):
    id_filter = set()
    async with aiosqlite.connect('parser.db') as db:
        for key in range(len(all_category_dict), 0, -1):
            for url in all_category_dict[str(key)].values():
                url = 'https://turbovent.com.ua/ua/g6989065-kanalnye-ventilyatory'  # !
                product: Product
                soup = BeautifulSoup(await fetch(session, url), 'lxml')
                total_pages = await _get_number_pages(soup)
                if not total_pages:
                    logger.warning(
                        f'{url} has no number_pages ({total_pages})')
                    continue
                print(f'{url} -> {total_pages=}')
                async for product in _get_all_products_on_page(soup, id_filter):
                    await single_product_processing(product, db)
                for num_page in range(2, total_pages+1):
                    async for product in _get_all_products_on_page(
                            BeautifulSoup(await fetch(session, url+f'/page_{num_page}'), 'lxml'),
                            id_filter):
                        await single_product_processing(product, db)
                        # all_products_data_dict.update(item)
                        # break
                    # break
                break
            break


async def _get_all_products_on_page(soup: BeautifulSoup, id_filter: set) -> Product:
    item: element.ResultSet
    for item in soup.find_all('li', class_='b-product-gallery__item'):
        yield await _make_one_product(item, id_filter)


async def single_product_processing(product: Product, db: aiosqlite.Connection):
    product_in_db = await get_product_from_db('suppliers',
                                              {'id_website': product.id},
                                              db)
    if not product_in_db:
        await db_add_product('suppliers',
                             product,
                             db)
    else:
        await check_product(product, product_in_db)
    with open('data/all_products.json', 'a', encoding='utf-8') as jsonfile:
        json.dump(
            {
                'id_website': product.id,
                'sku': product.sku,
                'title': product.title,
                'url': product.url,
                'price': product.price,
                'available': product.available

            },
            jsonfile, indent=4, ensure_ascii=False)


async def _make_one_product(item: element.ResultSet, id_filter: set) -> Product:
    id: str = await _get_product_id(item)
    if id is None and id in id_filter:
        return None
    id_filter.add(id)
    sku: str = await _get_product_sku(item, id)
    title: str = await _get_product_title(item, id)
    price: int = await _get_product_price(item, id)
    url: str = await _get_product_url(item, id)
    available: int = await _get_product_available(item, id)

    return Product(id, sku, title, price, url, available)


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
    regex = r"^[\s*\d*]+[\d+]+\s*грн\s*$"
    if price_text is None or re.match(regex, price_text.text) is None:
        logger.warning(f'{id} has no price')
        return 0
    return int(price_text.text.replace('\xa0', '').replace('грн', ''))


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
