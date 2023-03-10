# MessageCounterBot

Created by JawohlMeinHerr

Команды:
/echo - вывести пересланное боту в ЛС сообщение в консоль (для отладки)
/check_user - вывести статистику о пользователе, сообщение которого переслано
/add_new_admin - добавить пользователя, чье сообщение переслано, в список администраторов
/list_of_admins - вывести список айди пользователей-администраторов
/delete_admin - удалить администратора, чье сообщение переслано

База данных counter.db:
Таблица count
user_id TEXT
messages_count TEXT
symbols_count TEXT

Таблица admins
admin_id TEXT
