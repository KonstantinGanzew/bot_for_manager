import requests
import config

# Получаем ид сотрудника для ерпа
def get_id_erp(tel_id):
    url = config.URL_AUTH + str(tel_id)
    response = requests.get(url=url).json()
    return response['status']