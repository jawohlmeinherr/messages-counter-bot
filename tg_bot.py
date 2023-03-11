# Created from podval with love
# Author: github.com/jawohlmeinherr

from telebot import types
import telebot
import sqlite3

token = '6199924141:AAE9yarKSlNi-8wiVp6-aFX51E3ASKGZsCw'

bot = telebot.TeleBot(token)

db = sqlite3.connect('counter.db', check_same_thread=False)
sql = db.cursor()

sql.execute(""" CREATE TABLE IF NOT EXISTS count (
    user_id BIGINT,
    user_name TEXT,
    messages_count INT,
    symbols_count INT)""")
db.commit()

# echo
@bot.message_handler(commands=['echo'])
def echo(message):
    sql.execute("""SECELT * FROM admins""")
    r = sql.fetchall()

    amdins_ids = []

    for k in r:
        admins_ids.append(k[0])

    if message.from_user.id in admins_ids:
        msg = bot.reply_to(message, 'Перешли сообщение, объект которого нужно напечатать в консоль!')
        bot.register_next_step_handler(msg, echo_txt)
    else:
        bot.reply_to(message, 'У тебя нет прав для использования этой команды. Сорян!')

def echo_txt(message):
    print(message)
    bot.reply_to(message, 'Выведено в консоль!')

# add new admin
@bot.message_handler(commands=['add_new_admin'])
def receive_new_admin_id(message):
    sql.execute("""SELECT * FROM admins""")
    r = sql.fetchall()

    admins_ids = []

    for k in r:
        admins_ids.append(k[0])

    if message.from_user.id in admins_ids:
        msg = bot.reply_to(message, 'Перешли сообщение от того человека, которого хочешь назначить администратором бота!')
        bot.register_next_step_handler(msg, add_new_admin)
    else:
        bot.reply_to(message, 'У тебя нет прав для использования этой команд. Сорян!')

def add_new_admin(message):
    sql.execute("""INSERT INTO admins VALUES (?)""", (message.forward_from.id,))
    bot.reply_to(message, f'Добавлен новый администратор с id {message.forward_from.id}')

#list if admins
@bot.message_handler(commands=['list_of_admins'])
def list_of_admins(message):
    sql.execute("""SELECT * FROM admins""")
    r = sql.fetchall()

    admins_ids = []

    for k in r:
        admins_ids.append(k[0])

    if message.from_user.id in admins_ids:
        bot.reply_to(message, f'Список текущих администраторов: {admins_ids}')
    else:
        bot.reply_to(message, 'У тебя нет прав для использования этой команды. Сорян!')

# check user statistics
@bot.message_handler(commands=['check_user'])
def request_user_message(message):
    sql.execute("""SELECT * FROM admins""")
    r = sql.fetchall()

    admins_ids = []

    for k in r:
        admins_ids.append(k[0])

    if message.from_user.id in admins_ids:
        msg = bot.reply_to(message, 'Перешли сообщение человека, статистику по которому ты хочешь увидеть!')
        bot.register_next_step_handler(msg, check_user_statistics)
    else:
        bot.reply_to(message, 'У тебя нет прав для использования этой команды. Сорян!')

def check_user_statistics(message):
    sql.execute("""SELECT * FROM count WHERE user_id = ?""", (message.forward_from.id,))
    r = sql.fetchall()
    if len(r) != 0:
        bot.reply_to(message, f'Информация найдена!\n\nID пользователя: {r[0][0]}\nИмя пользователя: @{r[0][1]}\nСообщений: {r[0][2]}\nСимволов:{r[0][3]}')
    else:
        bot.reply_to(message, 'Этого пользователя нет в базе данных!')

# delete admin

@bot.message_handler(commands=['delete_admin'])
def request_admin_id(message):
    sql.execute("""SELECT * FROM admins""")
    r = sql.fetchall()

    admins_ids = []

    for k in r:
        admins_ids.append(k[0])

    if message.from_user.id in admins_ids:
        msg = bot.reply_to(message, 'Перешли сообщение человека, которого ты хочешь убрать из списка администраторов!')
        bot.register_next_step_handler(msg, delete_admin)
    else:
        bot.reply_to(message, 'У тебя нет прав для использования этой команды. Сорян!')

def delete_admin(message):
    sql.execute("""DELETE FROM admins WHERE admin_id = ?""", (message.forward_from.id,))
    db.commit()
    bot.reply_to(message, f'Администратор с id {message.forward_from.id} удален из списка администраторов!')

# adding data to database

@bot.message_handler(content_types=['text'])
def received_text(message):
    sql.execute("""SELECT user_id FROM count""")
    user_ids = sql.fetchall()
    users = []

    for k in user_ids:
        users.append(k[0])

    if message.from_user.id in users:
        sql.execute("""SELECT * FROM count WHERE user_id = ?""", (message.from_user.id,))
        user_data = sql.fetchall()
        sql.execute("""UPDATE count SET messages_count = ?, symbols_count = ? WHERE user_id = ?""", (user_data[0][2] + 1, user_data[0][3] + len(message.text), message.from_user.id))
        db.commit()
    else:
        sql.execute("""INSERT INTO count VALUES (?, ?, ?, ?)""", (message.from_user.id, message.from_user.username, 1, len(message.text),))
        db.commit()

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

try:
    bot.infinity_polling(); print('Bot started!')
except KeyboardInterrupt:
    print('Bot stopped!'); exit()
