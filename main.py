import csv
import json
import logging
import re
import sys
from urllib.parse import urlparse
import time

import requests
from bs4 import BeautifulSoup

from settings import headers

logger = logging.getLogger(__name__)
url = 'https://turbovent.com.ua/ua/product_list'
domen = urlparse(url)
domen = domen.scheme + '://' + domen.netloc


def make_soup(url: str, headers: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(url=url, headers=headers).text, 'lxml')


def make_all_categories_dict(soup: BeautifulSoup, all_categories_dict: dict, text: str) -> None:
    categories_list = soup.find_all(class_='b-product-groups-gallery__title')
    if not len(categories_list):
        return
    for category in categories_list:
        category_title = text + '/' + category.text if text != '' else category.text
        nesting_level = len(category_title.split('/'))
        category_url = domen + category.get('href')
        # print(category_title,
        #       category.get('href'))
        category_data_tuple = (category_title, category_url)
        # # print(cat)
        all_categories_dict.setdefault(nesting_level, [])
        all_categories_dict[nesting_level].append(category_data_tuple)
        # print(all_category_dict)
        # with open('data/all_category.csv', 'a', newline='') as csvfile:
        #     writer = csv.writer(
        #         csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        #     writer.writerow((category_title, category_url))

        make_all_categories_dict(make_soup(
            category_url, headers=headers), all_categories_dict, category_title)


def main():
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%d-%m-%y %H:%M:%S',
        format=u'%(asctime)s - [%(levelname)s] - (%(name)s).%(funcName)s:%(lineno)d - %(message)s',
        # filename='turbovent_parser.log'
    )
    #!
    try:
        response = requests.get(url=url, headers=headers)
        logger.info(f'parser get response (code={response.status_code}) from {url}')
    except requests.exceptions.ConnectionError as err:
        logger.error(f'parser get ConnectionError, url={url}')
        sys.exit(1)

    # with open('turbovent.html', 'w') as file:
    #     file.write(response.text)

    # with open('turbovent.html', 'r') as file:
    #     src = file.read()

    soup = BeautifulSoup(response.text, 'lxml')
    all_categories_dict = {}

    # with open('all_category.csv', 'w', newline = '') as csvfile:
    #     writer=csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
    #     writer.writerow(('category_title', 'category_url'))

    make_all_categories_dict(soup, all_categories_dict, '')

    # with open('data/all_categories.json', 'w', encoding='utf-8') as jsonfile:
    #     json.dump(all_category_dict, jsonfile, indent=4, ensure_ascii=False)

    # with open('data/all_categories.json', 'r', encoding='utf-8') as file:
    #     all_categories_dict = json.load(file)

    # print(all_categories_dict)
    # for key in range(len(all_categories_dict.keys()), 0, -1):
    #     # type_key = type(all_categories_dict.keys()[0])
    #     for link in all_categories_dict[key]:
    #         print(link[1])

#     products_in_main_page = soup.find_all(
#         'li', class_='b-product-gallery__item')

#     item_count = 0
#     for item in products_in_main_page:
#         if item_count == 0:

#             item_id = item.get('data-product-id')
#             item_sku = item.find(
#                 'span', class_='b-product-gallery__sku').text
#             item_title = item.find(
#                 class_='b-product-gallery__image-link').get('title')
#             item_url = domen + item.find(
#                 class_='b-product-gallery__image-link').get('href')
#             item_price = item.find(class_='b-goods-price').text
#             item_availability = item.find(
#                 'span', class_='b-goods-data__state').text

#             print(item_sku, item_id, item_title,
#                   item_url, item_price, item_availability)
#             break

#         item_count += 1

#     categories_in_main_page = ...


if __name__ == '__main__':
    start = time.time() ## точка отсчета времени
    main()
    end = time.time() - start ## собственно время работы программы
    print(end) ## вывод времени
