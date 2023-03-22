import csv
import json
import logging
import re
import sys
from urllib.parse import urlparse
import asyncio
import aiohttp
from functools import partial
import time
import async_timeout

import lxml
import requests
from bs4 import BeautifulSoup

from settings import headers, cookies

logger = logging.getLogger(__name__)
url = 'https://turbovent.com.ua/ua/product_list'
domen = urlparse(url)
domen = domen.scheme + '://' + domen.netloc
FETCH_TIMEOUT = 10


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
    for category in categories_list:
        category_title = text + '/' + category.text if text != '' else category.text
        nesting_level = len(category_title.split('/'))
        category_url = domen + category.get('href')
        category_data = (category_title, category_url)
        # print(cat)
        all_category_dict.setdefault(nesting_level, [])
        all_category_dict[nesting_level].append(category_data)
        tasks.append(make_all_categories_data_dict(
            category_url,
            session,
            all_category_dict,
            category_title
        ))
    await asyncio.gather(*tasks)


async def main():
    # loop = asyncio.get_event_loop()
    all_category_dict = {}
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        try:
            # await make_all_categories_data_dict(url,
            #                                     session,
            #                                     all_category_dict,
            #                                     '')

            # with open('data/all_categories.json', 'w', encoding='utf-8') as file:
            #     json.dump(all_category_dict, file, indent=4, ensure_ascii=False)

            # with open('data/all_categories.json', 'r') as file:
            #     all_category_dict = json.load(file)

            # count = 0
            # for key in range(len(all_category_dict.keys()), 0, -1):
            #     # for category in all_category_dict[str(key)]:
            #     #     print(category)
            #     # while count < 3:
            #     async for data in (await fetch(session, url[-1]) for url in all_category_dict[str(key)]):
            #         with open('one_product.html', 'w') as file:
            #             file.write(data)
            #         break
            #     #     count += 1
            #     break
            with open('one_product.html', 'r') as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')

            item_data = {
                item.find('a', class_='b-online-edit__link').get('data-edit-id'):
                (item.find('span', class_='b-product-gallery__sku').text.strip(),
                 item.find('a', class_='b-goods-title').text.strip(),
                 item.find(
                     'span', class_='b-goods-price__value').text.replace('\xa0', '').replace('грн', ''),
                 domen +
                 item.find('a', class_='b-goods-title').get('href').strip(),
                 item.find('span', class_='b-goods-data__state').text.strip())
                for item in soup.find_all('li', class_='b-product-gallery__item')}
            print(item_data)

        except Exception as err:
            logger.error(f'err: {err.args}')


if __name__ == '__main__':
    start = time.time()  # точка отсчета времени
    asyncio.run(main())
    end = time.time() - start  # собственно время работы программы
    print(end)  # вывод времени

# async def async_get_response(loop, url: str, headers: str) -> requests.Response:
#     func = partial(requests.get, url=url, headers=headers)
#     # print(url)
#     return await loop.run_in_executor(None, func)


# async def get_all_categories(loop, soup: BeautifulSoup, all_category_dict: dict, text: str) -> None:
#     categories_list = soup.find_all(class_='b-product-groups-gallery__title')
#     if not len(categories_list):
#         return
#     for category in categories_list:
#         category_title = text + '/' + category.text if text != '' else category.text
#         nesting_level = len(category_title.split('/'))
#         category_url = domen + category.get('href')
#         print(category_title,
#                 category.get('href'))
#         # cat = (category_title, category_url)
#         # # print(cat)
#         # all_category_dict.setdefault(nesting_level, [])
#         # all_category_dict[nesting_level].append(cat)
#         # print(all_category_dict)
#         # with open('data/all_category.csv', 'a', newline='') as csvfile:
#         #     writer = csv.writer(
#         #         csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
#         #     writer.writerow((category_title, category_url))
#         # resp = await async_get_response(
#         #     loop=loop, url=category_url, headers=headers)
#         resp = await async_get_response(
#             loop=loop, url=category_url, headers=headers)
#         await get_all_categories(loop, BeautifulSoup(resp.text, 'lxml'),
#             all_category_dict, category_title)


# async def main():
#     loop = asyncio.get_running_loop()
#     logging.basicConfig(
#         level=logging.INFO,
#         datefmt='%d-%m-%y %H:%M:%S',
#         format=u'%(asctime)s - [%(levelname)s] - (%(name)s).%(funcName)s:%(lineno)d - %(message)s',
#         # filename='regbot.log'
#     )
#     #!
#     try:
#         response = await async_get_response(loop, url=url, headers=headers)
#         logger.info(
#             f'parser get response (code={response.status_code}) from {url}')
#     except requests.exceptions.ConnectionError as err:
#         logger.error(f'parser get ConnectionError, url={url}')
#         sys.exit(1)

#     # with open('turbovent.html', 'w') as file:
#     #     file.write(response.text)

#     # text = '/'
#     all_category_dict = {}

#     # with open('turbovent.html', 'r') as file:
#     #     src = file.read()
#     soup = BeautifulSoup(response.text, 'lxml')
#     # with open('all_category.csv', 'w', newline = '') as csvfile:
#     #     writer=csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
#     #     writer.writerow(('category_title', 'category_url'))

#     await get_all_categories(loop, soup, all_category_dict, '')

#     # with open('data/all_categories.json', 'w', encoding='utf-8') as jsonfile:
#     #     json.dump(all_category_dict, jsonfile, indent=4, ensure_ascii=False)

#     # with open('data/all_categories.json', 'r', encoding='utf-8') as file:
#     #     all_categories_dict = json.load(file)

#     # print(all_categories_dict)
#     # for key in range(len(all_categories_dict.keys()), 0, -1):
#     #     for link in all_categories_dict[str(key)]:
#     #         print(link[1])

# #     products_in_main_page = soup.find_all(
# #         'li', class_='b-product-gallery__item')

# #     item_count = 0
# #     for item in products_in_main_page:
# #         if item_count == 0:

# #             item_id = item.get('data-product-id')
# #             item_sku = item.find(
# #                 'span', class_='b-product-gallery__sku').text
# #             item_title = item.find(
# #                 class_='b-product-gallery__image-link').get('title')
# #             item_url = domen + item.find(
# #                 class_='b-product-gallery__image-link').get('href')
# #             item_price = item.find(class_='b-goods-price').text
# #             item_availability = item.find(
# #                 'span', class_='b-goods-data__state').text

# #             print(item_sku, item_id, item_title,
# #                   item_url, item_price, item_availability)
# #             break

# #         item_count += 1

# #     categories_in_main_page = ...


# if __name__ == '__main__':
#     asyncio.run(main())
