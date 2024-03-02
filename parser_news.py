import requests as req
from bs4 import BeautifulSoup as Bs
from re import match
from sqlite3 import connect
import schedule

connection = connect("db.sqlite3")
cursor = connection.cursor()
starter = 61810
url = "https://stopgame.ru/news/all/p1"
url_news = "https://stopgame.ru"


def func(string: str):
    if isinstance(string, str):
        return bool(match(r'\d+', string))
    return False


def get_data():
    global starter
    result = req.get(url)
    bs = Bs(result.text, "html.parser")
    found = bs.find_all('div', attrs={'data-key': func})
    for element in found[::-1]:
        key = int(element['data-key'])
        if key > starter:
            starter = key
            data = element.find('a', class_='_title_11mk8_60')
            title = data.get_text()
            src = url_news + data['href']
            img_src = element.find('img')['src']
            cursor.execute(f'INSERT INTO Forum_news VALUES ("{starter}", "{title}", "{src}", "{img_src}", 1)')
            connection.commit()


schedule.every(15).minutes.do(get_data)

while True:
    schedule.run_pending()
