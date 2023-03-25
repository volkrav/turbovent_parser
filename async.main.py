import asyncio
import csv
import json
import logging
import re
import sys
import time

import aiohttp
from bs4 import BeautifulSoup

from misc.utils import fetch, make_all_categories_data_dict, make_all_products_data_dict
from settings import *

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%d-%m-%y %H:%M:%S',
        format=u'%(asctime)s - [%(levelname)s] - (%(name)s).%(funcName)s:%(lineno)d - %(message)s',
        # filename='turbovent_parser.log'
    )

    all_category_dict = {}
    all_products_data_dict = {}
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        try:
            await make_all_categories_data_dict(url,
                                                session,
                                                all_category_dict,
                                                '')

        #     with open('data/all_categories.json', 'w', encoding='utf-8') as file:
        #         json.dump(all_category_dict, file,
        #                   indent=4, ensure_ascii=False)

            # with open('data/all_categories.json', 'r') as file:
            #     all_category_dict = json.load(file)

            # await make_all_products_data_dict(all_products_data_dict, all_category_dict, session)

            # with open('data/all_products.json', 'w', encoding='utf-8') as file:
            #     json.dump(all_products_data_dict, file,
            #               indent=4, ensure_ascii=False)

            with open('data/all_products.json', 'r', encoding='utf-8') as file:
                all_category_dict = json.load(file)

            for items in all_category_dict:
                if all_category_dict.get(items).get('sku') == f'{items} has no sku':
                    print(all_category_dict.get(items).get('title'))



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
