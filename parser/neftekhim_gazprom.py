import requests
import math
import sql as sq

HOST = 'https://salavat-neftekhim.gazprom.ru'
URL = 'https://salavat-neftekhim.gazprom.ru/IMP-tenders?p=0&type=active&is_days_homepage=true'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
           'accept': '*/*'}

# Проверка доступности хоста

def get_status(url) -> bool:
    return requests.get(url, headers=HEADERS).status_code == 200

# Парсим салаватский газпром

def parsing_to_sql():
    response = requests.get(URL, headers=HEADERS).json()
    count = response['content']['main']['paging']['count']
    limit = response['content']['main']['paging']['limit']
    count_pages = math.ceil(count / limit)
    for item in range(count_pages):
        URL = f'https://salavat-neftekhim.gazprom.ru/IMP-tenders?p={item}&type=active&is_days_homepage=true'
        response = requests.get(URL, headers=HEADERS).json()
        limit = response['content']['main']['paging']['limit']
        offset = response['content']['main']['paging']['offset']
        if count - offset < limit:
            limit = count - offset
        for i in range(limit):
            id = response['content']['main']['tenders'][i]['id']
            href = HOST + response['content']['main']['tenders'][i]['href']
            name = response['content']['main']['tenders'][i]['name']
            description = response['content']['main']['tenders'][i]['description']
            dateEnd = response['content']['main']['tenders'][i]['dateEnd']
            dateEndYear = dateEnd['year']
            dateEndMonth = dateEnd['month']
            dateEndDay = dateEnd['day']
            dateStart = response['content']['main']['tenders'][i]['dateStart']
            dateStartYear = dateStart['year']
            dateStartMonth = dateStart['month']
            dateStartDay = dateStart['day']
            try:
                id_tenderSubject = int(response['content']['main']['tenders'][i]['tenderSubject']['id'])
                tenderSubject = response['content']['main']['tenders'][i]['tenderSubject']['name']
            except:
                id_tenderSubject = 99
                tenderSubject = 'Предмет закупки, не известен'
            sq.add_tend(int(id), name, description, href, f'{dateStartDay}.{dateStartMonth}.{dateStartYear}', f'{dateEndDay}.{dateEndMonth}.{dateEndYear}', id_tenderSubject, tenderSubject, 1, 1)

