import aiohttp
import async_timeout
import logging
from bs4 import BeautifulSoup
import asyncio

from settings import *


logger = logging.getLogger(__name__)


async def fetch(session, url):
    # print("run fetch")
    """
        Получаем URL страницу используя aiohttp, который возвращает html.
        Как полагается в документации aiohttp мы используем сессию повторно.
    """
    async with async_timeout.timeout(FETCH_TIMEOUT):
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as err:
            logger.error(f'err: {err.args}')


async def make_all_categories_data_dict(url, session, all_category_dict: dict, text: str) -> None:
    soup = BeautifulSoup(await fetch(session, url), 'lxml')
    categories_list = soup.find_all(class_='b-product-groups-gallery__title')
    if not len(categories_list):
        return
    tasks = []
    try:
        for category in categories_list:
            category_title = text + '/' + category.text if text != '' else category.text
            nesting_level = len(category_title.split('/'))
            category_url = domen + category.get('href')
            category_data = {category_title: category_url}
            # print(cat)
            all_category_dict.setdefault(str(nesting_level), {})
            all_category_dict[str(nesting_level)].update(category_data)
            tasks.append(make_all_categories_data_dict(
                category_url,
                session,
                all_category_dict,
                category_title
            ))
        await asyncio.gather(*tasks)
    except Exception as err:
        logger.error(f'{err.args}')

async def make_all_products_data_dict(all_products_data_dict: dict, all_category_dict: dict, session: aiohttp.ClientSession):
    for key in range(len(all_category_dict.keys()), 0, -1):
        async for data in (await fetch(session, url) for url in all_category_dict[str(key)].values()):
            # print(data)
            # break
            soup = BeautifulSoup(data, 'lxml')

            for item in soup.find_all('li', class_='b-product-gallery__item'):
                if item.find('a', class_='b-online-edit__link').get('data-edit-id') not in all_products_data_dict.keys():
                    id = item.find(
                        'a', class_='b-online-edit__link').get('data-edit-id')
                    try:
                        sku = item.find(
                            'span', class_='b-product-gallery__sku').text.strip() or ''
                    except AttributeError:
                        sku = ''
                        logger.warning(f'{id} has no sku')
                    try:
                        title = item.find(
                            'a', class_='b-goods-title').text.strip()
                    except AttributeError:
                        title = ''
                        logger.warning(f'{id} has no title')
                    try:
                        price = item.find(
                            'span', class_='b-goods-price__value').text.replace('\xa0', '').replace('грн', '')
                    except AttributeError:
                        price = ''
                        logger.warning(f'{id} has no price')
                    try:
                        url = domen + item.find(
                            'a', class_='b-goods-title').get('href').strip()
                    except AttributeError:
                        url = ''
                        logger.warning(f'{id} has no url')
                    try:
                        available = item.find(
                            'span', class_='b-goods-data__state').text.strip()
                    except AttributeError:
                        available = None
                        logger.warning(f'{id} has no available')
                    all_products_data_dict.update(
                        {id: {
                            'sku': sku,
                            'title': title,
                            'price': price,
                            'url': url,
                            'available': available
                        }
                        }
                    )
