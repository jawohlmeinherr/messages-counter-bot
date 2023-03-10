from telebot import types
import telebot
import sqlite3

users_whitelist = [1619385320, 600204669]

token = '6199924141:AAE9yarKSlNi-8wiVp6-aFX51E3ASKGZsCw'

bot = telebot.TeleBot(token)

db = sqlite3.connect('counter.db', check_same_thread=False)
sql = db.cursor()

sql.execute(""" CREATE TABLE IF NOT EXISTS count (
    user_id TEXT,
    messages_count TEXT,
    symbols_count TEXT)""")
db.commit()

# echo
@bot.message_handler(commands=['echo'])
def echo(message):
    if message.from_user.id in users_whitelist:
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
    if message.from_user.id in users_whitelist:
        msg = bot.reply_to(message, 'Перешли сообщение от того человека, которого хочешь назначить администратором бота!')
        bot.register_next_step_handler(msg, add_new_admin)
    else:
        bot.reply_to(message, 'У тебя нет прав для использования этой команд. Сорян!')

def add_new_admin(message):
    users_whitelist.append(message.forward_from.id)
    bot.reply_to(message, f'Добавлен новый администратор с id {message.forward_from.id}')

#list if admins
@bot.message_handler(commands=['list_of_admins'])
def list_of_admins(message):
    if message.from_user.id in users_whitelist:
        bot.reply_to(message, f'Список текущих администраторов: {users_whitelist}')
    else:
        bot.reply_to(message, 'У тебя нет прав для использования этой команды. Сорян!')

# check user statistics
@bot.message_handler(commands=['check_user'])
def request_user_message(message):
    if message.from_user.id in users_whitelist:
        msg = bot.reply_to(message, 'Перешли сообщение человека, статистику по которому ты хочешь увидеть!')
        bot.register_next_step_handler(msg, check_user_statistics)
    else:
        bot.reply_to(message, 'У тебя нет прав для использования этой команды. Сорян!')

def check_user_statistics(message):
    sql.execute("""SELECT * FROM count WHERE user_id = ?""", (str(message.forward_from.id),))
    r = sql.fetchall()
    if len(r) != 0:
        bot.reply_to(message, f'user_id: {r[0][0]}\nmessages: {r[0][1]}\nsymbols:{r[0][2]}')
    else:
        bot.reply_to(message, 'Этого пользователя нет в базе данных!')

# adding data to database

@bot.message_handler(content_types=['text'])
def received_text(message):
    sql.execute("""SELECT user_id FROM  count""")
    user_ids = sql.fetchall()
    users = []

    for k in user_ids:
        users.append(k[0])

    if str(message.from_user.id) in users:
        sql.execute("""SELECT * FROM count WHERE user_id = ?""", (str(message.from_user.id),))
        user_data = sql.fetchall()
        new_user_id = str(message.from_user.id)
        new_messages_count = str(int(user_data[0][1]) + 1)
        new_symbols_count = str(int(user_data[0][2]) + len(message.text))
        sql.execute("""UPDATE count SET messages_count = ?, symbols_count = ? WHERE user_id = ?""", (new_messages_count, new_symbols_count, new_user_id))
        db.commit()
    else:
        new_user_id = str(message.from_user.id)
        new_messages_count = '1'
        new_symbols_count = str(len(message.text))
        sql.execute("""INSERT INTO count VALUES (?, ?, ?)""", (new_user_id, new_messages_count, new_symbols_count,))
        db.commit()

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

try:
    bot.infinity_polling(); print('Bot started!')
except KeyboardInterrupt:
    print('Bot stopped!'); exit()
