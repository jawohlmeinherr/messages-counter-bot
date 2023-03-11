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
user_id BIGINT (айди юзера)
user_name TEXT (имя юзера)
messages_count INT (кол-во сообщений)
symbols_count INT (кол-во символов)

Таблица admins
admin_id BIGINT (айди юзера)

11-Mar-2023 
Последние изменения:
- немного переписан код в более приятный вид
- теперь в таблице не все хранится текстом, а добавлены строки с численными типами данных
- добавлена колонка user_name (которая с собачки в телеге) и немного изменен вывод информации о пользователе

TO-DO:
- перенести базу данных на другую (sqlite3 не многопоточная, бот сваливаетс и некоторое время не обрабатывает сообщения когда их отправляют одновременно разные пользователи. ошибка sqlite3.ProgrammingError: Recursive use of cursors not allowed.)
Переносить лучше на PostgreSQL
