import asyncio
import json
import logging
import sys
import time
import aiofiles

import aiohttp

import settings
from data.db_api import db_create_tables
from handlers.categories import make_all_categories_data_dict
from handlers.products import make_all_products_data_dict

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%d-%m-%y %H:%M:%S',
        format=u'%(asctime)s - [%(levelname)s] - (%(name)s).%(funcName)s:%(lineno)d - %(message)s',
        # filename='turbovent_parser.log'
    )
    await db_create_tables()

    async with aiohttp.ClientSession(headers=settings.headers) as session:
        match sys.argv:
            case _, 'parsecat' as command:
                logger.info(f'got the command to parse categories. {command=}')
                all_category_dict = await make_all_categories_data_dict(
                    settings.url,
                    session,
                )
                async with aiofiles.open('data/all_categories.json', 'w', encoding='utf-8') as file:
                    json_data = json.dumps(all_category_dict,
                                        indent=4, ensure_ascii=False)
                    await file.write(json_data)
            case _:
                async with aiofiles.open('data/all_categories.json', 'r') as file:
                    json_contents = await file.read()
                    all_category_dict = json.loads(json_contents)

        # all_products_data_dict = await make_all_products_data_dict(all_category_dict, session)

        # with open('data/all_products.json', 'w', encoding='utf-8') as file:
        #     json.dump(all_products_data_dict, file,
        #               indent=4, ensure_ascii=False)


if __name__ == '__main__':
    start = time.time()  # точка отсчета времени
    asyncio.run(main())
    end = time.time() - start  # собственно время работы программы
    print(end)  # вывод времени
