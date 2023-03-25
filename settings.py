from urllib.parse import urlparse


url = 'https://turbovent.com.ua/ua/product_list'
domen = urlparse(url)
domen = domen.scheme + '://' + domen.netloc

FETCH_TIMEOUT = 10



cookies = {
    'evoauth': 'wb12d94ed79c64e89aced1222d2478309',
    'csrf_token_company_site': '4107177a223d4991873be09a72aa1f82',
    'cid': '213679216316924220840283534485372554603',
    'companies_visited_products': '283048327.1016566918.1017088762.147301099.655773805.1017088975.1304610271.1652084729.172786084.',
    'ccc': 'ZB9at9RaJzZNLAh5UEtPJaSKUJh3IlSt4pcUtnMwJUplZFKkYJv9mLVjpmj6S6bDXnRO_MyzEyfSOAY54Mw8EA==',
    'biatv-cookie': '{%22firstVisitAt%22:1675431573%2C%22visitsCount%22:13%2C%22campaignCount%22:1%2C%22currentVisitStartedAt%22:1679517240%2C%22currentVisitLandingPage%22:%22https://turbovent.com.ua/ua/%22%2C%22currentVisitOpenPages%22:2%2C%22location%22:%22https://turbovent.com.ua/ua/%22%2C%22locationTitle%22:%22%D0%92%D0%B5%D0%BD%D1%82%D0%B8%D0%BB%D1%8F%D1%86%D1%96%D0%B9%D0%BD%D1%96%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B8%20|%20%D0%9A%D1%83%D0%BF%D0%B8%D1%82%D0%B8%20%D0%BF%D1%80%D0%BE%D0%BC%D0%B8%D1%81%D0%BB%D0%BE%D0%B2%D1%96%20%D0%B2%D0%B5%D0%BD%D1%82%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B8%20|%20turbovent.com.ua%22%2C%22userAgent%22:%22Mozilla/5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML%2C%20like%20Gecko)%20Chrome/111.0.0.0%20Safari/537.36%22%2C%22language%22:%22ru-ru%22%2C%22encoding%22:%22utf-8%22%2C%22screenResolution%22:%221920x1080%22%2C%22currentVisitUpdatedAt%22:1679517453%2C%22utmDataCurrent%22:{%22utm_source%22:%22(direct)%22%2C%22utm_medium%22:%22(none)%22%2C%22utm_campaign%22:%22(direct)%22%2C%22utm_content%22:%22(not%20set)%22%2C%22utm_term%22:%22(not%20set)%22%2C%22beginning_at%22:1675431573}%2C%22campaignTime%22:1675431573%2C%22utmDataFirst%22:{%22utm_source%22:%22(direct)%22%2C%22utm_medium%22:%22(none)%22%2C%22utm_campaign%22:%22(direct)%22%2C%22utm_content%22:%22(not%20set)%22%2C%22utm_term%22:%22(not%20set)%22%2C%22beginning_at%22:1675431573}%2C%22geoipData%22:{%22country%22:%22Ukraine%22%2C%22region%22:%22Kyiv%20City%22%2C%22city%22:%22Kyiv%22%2C%22org%22:%22%22}}',
    'bingc-activity-data': '{%22numberOfImpressions%22:0%2C%22activeFormSinceLastDisplayed%22:6%2C%22pageviews%22:2%2C%22callWasMade%22:0%2C%22updatedAt%22:1679517457}',
}

headers = {
    'authority': 'turbovent.com.ua',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'evoauth=wb12d94ed79c64e89aced1222d2478309; csrf_token_company_site=4107177a223d4991873be09a72aa1f82; cid=213679216316924220840283534485372554603; companies_visited_products=283048327.1016566918.1017088762.147301099.655773805.1017088975.1304610271.1652084729.172786084.; ccc=ZB9at9RaJzZNLAh5UEtPJaSKUJh3IlSt4pcUtnMwJUplZFKkYJv9mLVjpmj6S6bDXnRO_MyzEyfSOAY54Mw8EA==; biatv-cookie={%22firstVisitAt%22:1675431573%2C%22visitsCount%22:13%2C%22campaignCount%22:1%2C%22currentVisitStartedAt%22:1679517240%2C%22currentVisitLandingPage%22:%22https://turbovent.com.ua/ua/%22%2C%22currentVisitOpenPages%22:2%2C%22location%22:%22https://turbovent.com.ua/ua/%22%2C%22locationTitle%22:%22%D0%92%D0%B5%D0%BD%D1%82%D0%B8%D0%BB%D1%8F%D1%86%D1%96%D0%B9%D0%BD%D1%96%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B8%20|%20%D0%9A%D1%83%D0%BF%D0%B8%D1%82%D0%B8%20%D0%BF%D1%80%D0%BE%D0%BC%D0%B8%D1%81%D0%BB%D0%BE%D0%B2%D1%96%20%D0%B2%D0%B5%D0%BD%D1%82%D0%B8%D0%BB%D1%8F%D1%82%D0%BE%D1%80%D0%B8%20|%20turbovent.com.ua%22%2C%22userAgent%22:%22Mozilla/5.0%20(Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7)%20AppleWebKit/537.36%20(KHTML%2C%20like%20Gecko)%20Chrome/111.0.0.0%20Safari/537.36%22%2C%22language%22:%22ru-ru%22%2C%22encoding%22:%22utf-8%22%2C%22screenResolution%22:%221920x1080%22%2C%22currentVisitUpdatedAt%22:1679517453%2C%22utmDataCurrent%22:{%22utm_source%22:%22(direct)%22%2C%22utm_medium%22:%22(none)%22%2C%22utm_campaign%22:%22(direct)%22%2C%22utm_content%22:%22(not%20set)%22%2C%22utm_term%22:%22(not%20set)%22%2C%22beginning_at%22:1675431573}%2C%22campaignTime%22:1675431573%2C%22utmDataFirst%22:{%22utm_source%22:%22(direct)%22%2C%22utm_medium%22:%22(none)%22%2C%22utm_campaign%22:%22(direct)%22%2C%22utm_content%22:%22(not%20set)%22%2C%22utm_term%22:%22(not%20set)%22%2C%22beginning_at%22:1675431573}%2C%22geoipData%22:{%22country%22:%22Ukraine%22%2C%22region%22:%22Kyiv%20City%22%2C%22city%22:%22Kyiv%22%2C%22org%22:%22%22}}; bingc-activity-data={%22numberOfImpressions%22:0%2C%22activeFormSinceLastDisplayed%22:6%2C%22pageviews%22:2%2C%22callWasMade%22:0%2C%22updatedAt%22:1679517457}',
    'referer': 'https://turbovent.com.ua/ua/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}
