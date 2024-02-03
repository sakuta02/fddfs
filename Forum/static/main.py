import requests as req
from bs4 import BeautifulSoup as Bs
from re import match
import sqlite3

con = sqlite3.connect('../../db.sqlite3')
cur = con.cursor()


def func(string: str):
    if type(string) == str:
        return bool(match(r'\d+', string))
    return False


url = "https://stopgame.ru/news/all/p"
url_news = "https://stopgame.ru"

index = 0
for i in range(1, 6):
    result = req.get(url + str(i))
    bs = Bs(result.text, "html.parser")
    found = bs.find_all('div', attrs={'data-key': func})
    for element in found:
        index += 1
        data = element.find('a', class_='_title_11mk8_60')
        title = data.get_text()
        src = url_news + data['href']
        img_src = element.find('img')['src']
        img = req.get(img_src).content
        genre = 'Made by StopGame'
