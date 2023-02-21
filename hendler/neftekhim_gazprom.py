import requests
import math

HOST = 'https://salavat-neftekhim.gazprom.ru'
URL = 'https://salavat-neftekhim.gazprom.ru/IMP-tenders?p=0&type=active&is_days_homepage=true'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
           'accept': '*/*'}

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
        dateYear = dateEnd['year']
        dateMonth = dateEnd['month']
        dateDay = dateEnd['day']
        print(f'id: {id}\n{name}\n{description}\n{href}\nДата закрытия тендера: {dateDay}.{dateMonth}.{dateYear}\n')
    print(f'Страница {item}, Количество элемнтов {limit}')