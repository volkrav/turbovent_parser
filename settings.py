import requests

cookies = {
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_first_add': 'fd%3D2022-11-02%2012%3A32%3A09%7C%7C%7Cep%3Dhttps%3A%2F%2Felectrokom.kiev.ua%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'intercom-device-id-xr5cw062': '39af78c7-2e6a-4449-8f59-303080d44757',
    'sbjs_current_add': 'fd%3D2022-11-22%2010%3A45%3A03%7C%7C%7Cep%3Dhttps%3A%2F%2Felectrokom.kiev.ua%2Fproduct%2Fventilyator_kanalnyy_vk-100%3Futm_source%3Dgoogle%26utm_medium%3Dcpc%26utm_campaign%3D%25D0%25A2%25D0%25BE%25D1%2580%25D0%25B3%25D0%25BE%25D0%25B2%25D0%25B0%25D1%258F%2520%25D0%25BF%25D1%2580%25D0%25BE%25D1%2581%25D1%2582%25D0%25B0%25D1%258F%2520-%2520%25D0%2592%25D1%2581%25D0%25B5%2520%25D1%2582%25D0%25BE%25D0%25B2%25D0%25B0%25D1%2580%25D1%258B%26utm_term%3D%26gclid%3DCj0KCQiA4OybBhCzARIsAIcfn9m122CBBdzlF6fxULCRjUBJ_zCNevcj5MUrxVYQuQ-6VdB8191KmhkaAuwLEALw_wcB%7C%7C%7Crf%3D%28none%29',
    'sbjs_current': 'typ%3Dutm%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dcpc%7C%7C%7Ccmp%3D%25D0%25A2%25D0%25BE%25D1%2580%25D0%25B3%25D0%25BE%25D0%25B2%25D0%25B0%25D1%258F%2520%25D0%25BF%25D1%2580%25D0%25BE%25D1%2581%25D1%2582%25D0%25B0%25D1%258F%2520-%2520%25D0%2592%25D1%2581%25D0%25B5%2520%25D1%2582%25D0%25BE%25D0%25B2%25D0%25B0%25D1%2580%25D1%258B%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'PHPSESSID': '2s2bqd4jl4khrulko5tdhci973',
    'uuid': '206362cd5985477f3491ce14301da8f2',
    'sbjs_udata': 'vst%3D99%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F111.0.0.0%20Safari%2F537.36',
    'sbjs_session': 'pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Felectrokom.kiev.ua%2Fcatalog%2Fkatalog',
}

headers = {
    'authority': 'electrokom.kiev.ua',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'sbjs_migrations=1418474375998%3D1; sbjs_first_add=fd%3D2022-11-02%2012%3A32%3A09%7C%7C%7Cep%3Dhttps%3A%2F%2Felectrokom.kiev.ua%2F%7C%7C%7Crf%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; intercom-device-id-xr5cw062=39af78c7-2e6a-4449-8f59-303080d44757; sbjs_current_add=fd%3D2022-11-22%2010%3A45%3A03%7C%7C%7Cep%3Dhttps%3A%2F%2Felectrokom.kiev.ua%2Fproduct%2Fventilyator_kanalnyy_vk-100%3Futm_source%3Dgoogle%26utm_medium%3Dcpc%26utm_campaign%3D%25D0%25A2%25D0%25BE%25D1%2580%25D0%25B3%25D0%25BE%25D0%25B2%25D0%25B0%25D1%258F%2520%25D0%25BF%25D1%2580%25D0%25BE%25D1%2581%25D1%2582%25D0%25B0%25D1%258F%2520-%2520%25D0%2592%25D1%2581%25D0%25B5%2520%25D1%2582%25D0%25BE%25D0%25B2%25D0%25B0%25D1%2580%25D1%258B%26utm_term%3D%26gclid%3DCj0KCQiA4OybBhCzARIsAIcfn9m122CBBdzlF6fxULCRjUBJ_zCNevcj5MUrxVYQuQ-6VdB8191KmhkaAuwLEALw_wcB%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dutm%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dcpc%7C%7C%7Ccmp%3D%25D0%25A2%25D0%25BE%25D1%2580%25D0%25B3%25D0%25BE%25D0%25B2%25D0%25B0%25D1%258F%2520%25D0%25BF%25D1%2580%25D0%25BE%25D1%2581%25D1%2582%25D0%25B0%25D1%258F%2520-%2520%25D0%2592%25D1%2581%25D0%25B5%2520%25D1%2582%25D0%25BE%25D0%25B2%25D0%25B0%25D1%2580%25D1%258B%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; PHPSESSID=2s2bqd4jl4khrulko5tdhci973; uuid=206362cd5985477f3491ce14301da8f2; sbjs_udata=vst%3D99%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F111.0.0.0%20Safari%2F537.36; sbjs_session=pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Felectrokom.kiev.ua%2Fcatalog%2Fkatalog',
    'referer': 'https://electrokom.kiev.ua/',
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

response = requests.get('https://electrokom.kiev.ua/catalog/katalog', cookies=cookies, headers=headers)
