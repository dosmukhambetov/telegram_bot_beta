from aiogram import types, Dispatcher
from create_bot import bot, dp
from random import randrange
from keyboards import client_kb
from data_base import sq_db

COMMAND_HELP = """
Привет 👋, я бот по продаже различных товаров! У нас есть такие команды как:
**********************************************
<b>/start</b> - запуск бота 🚀
<b>/help</b> - помощь по командам бота 💬
<b>/products</b> - список товаров которые можно купить 📒
<b>/description</> - адрес, контактные данные, график работы 🕒
**********************************************
Команды Администратора:
<b>/admin</b> - проверка на администратора 🔐
<b>/download</b> - добавить новый товар 🎉
<b>/delete</b> - удалить товар из списка ❌
<b>/cancel</b> - отменить редактирование/создание товара ↩️
<b>/home</b> - перейти в главное меню 🏠
"""


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(chat_id=message.chat.id,
                               text="Привет ✋, я бот по продаже различных товаров! "
                                    "У меня вы можете купить все что захотите, чтобы увидеть список "
                                    "товаров которые у меня есть введите эту команду\n/products",
                               reply_markup=client_kb)
    except:
        await message.reply(text="Чтобы можно было общаться с ботом, "
                                 "ты можешь написать мне в личные сообщение: "
                                 "https://t.me/arcanashop_dota2_bot")


# @dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=COMMAND_HELP,
                           parse_mode="html")


# @dp.message_handler(commands=['products'])
async def command_cars(message: types.Message):
    await sq_db.command_sql_read_for_client(message)


# @dp.message_handler(commands=['description'])
async def command_description(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет ✋, мы компания по продаже различных товаров!, "
                                "Мы очень рады что Вы используете"
                                "наш сервис ❤️, мы работает с Понедельника до "
                                "Пятницы, 9:00 - 21:00")
    await bot.send_location(chat_id=message.chat.id,
                            latitude=randrange(1, 100),
                            longitude=randrange(1, 100))


def registration_clients_handlers(disp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_cars, commands=['products'])
    dp.register_message_handler(command_description, commands=['description'])
