import requests

def get_html(url)
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except requests.exceptions.RequestExeption:
        print ('Не получилось')
        return False


html = get_html('https://yandex.ru/search/?lr=213&msid=1492258299.59905.22879.9839&text=python')
print(html)