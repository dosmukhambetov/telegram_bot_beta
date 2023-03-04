from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from config import ADMIN_ID
from create_bot import dp, bot
from keyboards import admin_kb, client_kb
from data_base import sq_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# @dp.message_handler(commands=['home'])
async def command_home(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Вы перешли в главное меню!",
                             reply_markup=client_kb)


# @dp.message_handler(commands=['admin'])
async def command_admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.reply(text="Вы успешно прошли проверку на Администратора! 👑",
                            reply_markup=admin_kb)
    else:
        await message.reply("Вы не администратор и не сможете использовать команды администратора!")


# @dp.message_handler(commands=['download'], state=None)
async def command_download(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await FSMadmin.photo.set()
        await message.answer("Загрузи фото товара! 📦")


# @dp.message_handler(commands=['cancel'], state="*")
# @dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def command_cancel(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply(text="Операция успешно отменена. 🙅‍♂️")


# @dp.message_handler(content_types=['photo'], state=FSMadmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply("Теперь введи название товара! 💬")


# @dp.message_handler(state=FSMadmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.next()
        await message.reply("Ого, классно 😎, а теперь напиши подробное описание этого товара!")


# @dp.message_handler(state=FSMadmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMadmin.next()
        await message.reply("А теперь тебе нужно ввести сумму, за которую ты хочешь продать товар 💰")


# @dp.message_handler(state=FSMadmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await sq_db.command_sql_add(state)
        await message.answer("Объявление успешно добавлено 🌟. Чтобы посмотреть объявление напишите команду /products")
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del'))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sq_db.command_sql_delete(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} удалена успешно.",
                                show_alert=True)


# @dp.message_handler(commands=['delete'])
async def command_delete(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        read = await sq_db.command_sql_read_for_admin_delete()
        for ret in read:
            await bot.send_photo(message.chat.id, ret[0], f"{ret[1]}\nОписание: {ret[2]}\n Цена: {ret[-1]}")
            await bot.send_message(message.chat.id,
                                   text="Удалить вышерасположенный объект ⬆️",
                                   reply_markup=InlineKeyboardMarkup()
                                   .add(InlineKeyboardButton(f"Удалить {ret[1]}",
                                                             callback_data=f"del {ret[1]}")))


def registration_admin_handlers(disp: Dispatcher):
    dp.register_message_handler(command_home, commands=['home'])
    dp.register_message_handler(command_admin, commands=['admin'])
    dp.register_message_handler(command_download, commands=['download'], state=None)
    dp.register_message_handler(command_cancel, commands=['cancel'], state="*")
    dp.register_message_handler(command_cancel, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name)
    dp.register_message_handler(load_description, state=FSMadmin.description)
    dp.register_message_handler(load_price, state=FSMadmin.price)
    dp.register_message_handler(command_delete, commands=['delete'])
