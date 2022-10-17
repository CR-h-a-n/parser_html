import requests
from bs4 import BeautifulSoup
import pprint
import json


def parser_news(class_string):
    all_tr_news_set = soup.findAll('tr', class_=class_string)
    for one_tr_news in all_tr_news_set:
        time_news = one_tr_news.find('td', class_='first left time js-time')
        country = one_tr_news.find('td', class_='left flagCur noWrap')
        importance = one_tr_news.findAll('i', class_='grayFullBullishIcon')
        event_tag_td = one_tr_news.find('td', class_='left event')
        event_tag_a = event_tag_td.find('a')
        list_news.append({'time': time_news.text, 'country': country.text[-3:], 'importance': len(importance),
                          'event': event_tag_a.text[1:]})


url = 'https://ru.investing.com/economic-calendar/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
list_news = []

parser_news('js-event-item')
pprint.pprint(list_news)

result = json.dumps(list_news)
file_name = 'economic_calendar.json'
with open(file_name, 'w') as f:
    json.dump(result, f)

