import logging
import csv
import lxml
import re
from urllib.parse import urlparse
import sys

import requests
from bs4 import BeautifulSoup

from settings import headers

logger = logging.getLogger(__name__)
url = 'https://turbovent.com.ua/ua/product_list'
domen = urlparse(url)
domen = domen.scheme + '://' + domen.netloc


def get_all_categories(soup: BeautifulSoup, all_category_dict, text):
    categories_list = soup.find_all(class_='b-product-groups-gallery__title')
    if not len(categories_list):
        return
    for category in categories_list:
        category_title = text + '/' + category.text
        category_url = domen + category.get('href')
        print(category_title,
                category.get('href'))
        with open('all_category.csv', 'a', newline='') as csvfile:
            writer = csv.writer(
                csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow((category_title, category_url))

        get_all_categories(BeautifulSoup(requests.get(
            category_url, headers=headers).text, 'lxml'), all_category_dict, category_title)

    # {category.text: category.get('href')
    #                      for category in soup.find_all(
    #     class_='b-product-groups-gallery__title')}


def main():
    logging.basicConfig(
        level = logging.INFO,
        datefmt = '%d-%m-%y %H:%M:%S',
        format = u'%(asctime)s - [%(levelname)s] - (%(name)s).%(funcName)s:%(lineno)d - %(message)s',
        # filename='regbot.log'
    )
    # try:
    #     response = requests.get(url=url, headers=headers)
    #     logger.info(response.status_code)
    # except requests.exceptions.ConnectionError as err:
    #     logger.error(f'parser get ConnectionError, url={url}')
    #     sys.exit(1)

    # with open('turbovent.html', 'w') as file:
    #     file.write(response.text)

    text='/'
    all_category_dict={}

    with open('turbovent.html', 'r') as file:
        src=file.read()
    soup=BeautifulSoup(src, 'lxml')
    with open('all_category.csv', 'w', newline = '') as csvfile:
        writer=csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(('category_title', 'category_url'))

    get_all_categories(soup, all_category_dict, '')

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
    main()
