from aiogram import executor
from create_bot import dp
from handlers import client, admin
from data_base import sq_db


async def on_startup(_):
    print('Бот был успешно запущен;')
    sq_db.sql_start()


client.registration_clients_handlers(dp)
admin.registration_admin_handlers(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
