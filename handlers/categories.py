import asyncio
import logging

from bs4 import BeautifulSoup

import settings
from misc.utils import fetch


logger = logging.getLogger(__name__)


async def make_all_categories_data_dict(url, session) -> dict:
    all_category_dict = {}
    await _make_all_categories_data_dict(url, session, all_category_dict, '')
    return all_category_dict


async def _make_all_categories_data_dict(url, session, all_category_dict: dict, text: str) -> None:

    soup = BeautifulSoup(await fetch(session, url), 'lxml')
    categories_list = soup.find_all(class_='b-product-groups-gallery__title')
    if not len(categories_list):
        return
    tasks = []
    try:
        for category in categories_list:
            category_title = text + '/' + category.text if text != '' else category.text
            nesting_level = len(category_title.split('/'))
            category_url = settings.domen + category.get('href')
            category_data = {category_title: category_url}
            all_category_dict.setdefault(str(nesting_level), {})
            all_category_dict[str(nesting_level)].update(category_data)
            tasks.append(_make_all_categories_data_dict(
                category_url,
                session,
                all_category_dict,
                category_title
            ))
        await asyncio.gather(*tasks)
    except Exception as err:
        logger.error(f'{err.args}')
