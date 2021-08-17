import telebot
from bs4 import BeautifulSoup
import requests
import logging
from settings import TOKEN
from datetime import datetime
from telegram.ext import CommandHandler

###############парсер######################
url = 'https://www.liveinternet.ru/users/zapytay/post155075998'
logging.info(f'parsing {url}')

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

compliments = soup.findAll('p')
test = []
for data in compliments:
	if data.find('span') is not None:
		test.append(data.text)

test = test[98:]
test = [x[4:] for x in test]
################Класс пользователя#########
class User:
	registry = []

	def __init__(self, tg_id):
		self.tg_id = tg_id
		self.index = 0
		self.compliments = []
		self.registry.append(self)

	def get_user(tg_id):
		for user in User.registry:
			if user.tg_id == tg_id:
				return user

	def user_is_know(tg_id):
		for user in User.registry:
			if user.tg_id == tg_id:
				return True
		return False

##############Бот###########################
bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Получить комплимент')
    bot.send_message(message.chat.id, 'Привет, я создан для того, чтобы твои отношения стали чуть лучше <3', reply_markup=keyboard)

#def auto_message(message):
#	bot.send_message(message.chat.id, user.compliments[user.index])
#schedule.every().day.at('13:00').do(auto_message)
#while True:
#	schedule.run_pending()
#	time.sleep(1)

@bot.message_handler(content_types=['text'])
def message_text(message):
	user = User.get_user(message.chat.id)
	if user is None:
		user = User(message.chat.id)

	if message.text == 'Получить комплимент':
		if len(user.compliments) == 0:
			user.compliments = test
		bot.send_message(message.chat.id, user.compliments[user.index])
		user.index += 1
	else:
		bot.send_message(message.chat.id, 'Я тебя не понимаю, воспользуйся клавиатурой.')

	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	print("Current Time =", current_time)
	if current_time=='20:14:00':
		test_send_message()

	def test_send_message():
		user = User.get_user(message.chat.id)
		if user is None:
			user = User(message.chat.id)

		if len(user.compliments) == 0:
			user.compliments = test
		text = user.compliments[user.index]
		tb = telebot.TeleBot(TOKEN)
		ret_msg = bot.send_message(message.chat.id, user.compliments[user.index])
		user.index += 1
		assert ret_msg.message.chat.id


bot.polling(none_stop= True, interval=0)