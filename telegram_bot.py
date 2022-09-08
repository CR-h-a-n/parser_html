import requests
import telebot
from bs4 import BeautifulSoup
import pprint


TOKEN = '5678539181:AAGHl282z0hf01m9rZ8AtMJVkkvGcYM_4_o'
bot = telebot.TeleBot(TOKEN)


def take_soup():
	url = 'https://ru.investing.com/economic-calendar/'
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	return soup.findAll('tr', class_='js-event-item')


def list_ticket():
	list_country = {}
	all_tr_news_set = take_soup()
	for one_tr_news in all_tr_news_set:
		country_td = one_tr_news.find('td', class_='left flagCur noWrap')
		country_span = country_td.find('span')
		list_country[country_td.text[2:]] = country_span['title']
	list_country = dict(sorted(list_country.items(), key=lambda x: x[1]))
	message_country = 'Сегодня выходят новости по: '
	for country in list_country:
		message_country += list_country[country] + '(/'+country+'), '
	message_country = message_country[:-2] + '\n\n/all - вывод списка всех новостей.'
	return message_country


@bot.message_handler(commands=['list'])
def list_news(message):
	message_country = list_ticket()
	bot.send_message(message.chat.id, message_country)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	print(message)
	first_name = message.from_user.first_name
	bot.send_message(message.chat.id, first_name+', добрый день! \nВы запустили бот ''''Экономический календарь''''!')
	list_news(message)


@bot.message_handler(commands=['all'])
def send_all_news(message):
	all_tr_news_set = take_soup()
	message_all_news = ''
	for one_tr_news in all_tr_news_set:
		time_news = one_tr_news.find('td', class_='first left time js-time')
		country = one_tr_news.find('td', class_='left flagCur noWrap')
		importance = one_tr_news.findAll('i', class_='grayFullBullishIcon')
		event_tag_td = one_tr_news.find('td', class_='left event')
		event_tag_a = event_tag_td.find('a')
		message_all_news += time_news.text + ' ' + country.text[-3:] + '\nВажность: ' + '*'*len(importance) + '\n' + event_tag_a.text[1:] + '\n\n'
	bot.send_message(message.chat.id, message_all_news)


@bot.message_handler(commands=['help'])
def help_message_send(message):
	help_message = '/start - запуск бота\n' \
				   '/help - список доступных команд\n' \
				   '/list - список стран, по которым выходят новости\n' \
				   '/all - вывод всех новостей'
	bot.send_message(message.chat.id, help_message)


@bot.message_handler(content_types=['text'])
def take_country_news(message):
	all_tr_news_set = take_soup()
	country_flag = message.text[1:]
	# print(country_flag)
	country_name = 'Не понял ваш запрос.'
	message_all_news = ''
	for one_tr_news in all_tr_news_set:
		country_td = one_tr_news.find('td', class_='left flagCur noWrap')
		if country_td.text[-3:] == country_flag:
			time_news = one_tr_news.find('td', class_='first left time js-time')
			country_span = country_td.find('span')
			country_name = country_span['title']
			importance = one_tr_news.findAll('i', class_='grayFullBullishIcon')
			event_tag_td = one_tr_news.find('td', class_='left event')
			event_tag_a = event_tag_td.find('a')
			message_all_news += time_news.text + ' ' + country_td.text[-3:] + '\nВажность: ' + '*' * len(
				importance) + '\n' + event_tag_a.text[1:] + '\n\n'

	if country_name == 'Не понял ваш запрос.':
		bot.send_message(message.chat.id, country_name)
		list_news(message)
	else:
		message_all_news = country_name + ':\n\n' + message_all_news
		bot.send_message(message.chat.id, message_all_news)


bot.polling()
