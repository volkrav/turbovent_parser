import aiofiles
import aiohttp
import asyncio
import async_timeout


async def fetch(session, url, proxy):
    try:
        async with async_timeout.timeout(60):
            async with session.get(url=url, proxy=proxy) as response:
                if response.status == 200:
                    print(f'!!!!! i find working {proxy}')
                    return proxy
    except Exception as err:
        return None


async def main():
    async with aiofiles.open('misc/http.txt', 'r') as file:
        proxies = [f'http://{url.strip()}' for url in await file.readlines()]

    test_url = 'https://turbovent.com.ua/ua'
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, test_url, proxy)) for proxy in proxies]
        working_proxies = await asyncio.gather(*tasks)

    async with aiofiles.open('misc/workingproxies.txt', 'w', encoding='utf-8') as file:
        await file.write('\n'.join([url for url in working_proxies if isinstance(url, str) and url != '']))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
