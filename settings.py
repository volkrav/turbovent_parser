from urllib.parse import urlparse


url = 'https://turbovent.com.ua/ua/product_list'
_domen = urlparse(url)
domen = _domen.scheme + '://' + _domen.netloc

FETCH_TIMEOUT = 20
SLEEP_TIME = 5

prom_available_dict = {
    'В наявності': 1,
    'Під замовлення': 0,
    'На складі': 1,
    'Немає в наявності': 0
}

headers = {
    'authority': 'turbovent.com.ua',
    'method': 'GET',
    'path': '/ua/',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'cache-control': 'max-age = 0',
    'referer': 'https://turbovent.com.ua/ua/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}
