import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart 
from config import TOKEN
from aiogram.types import BotCommandScopeAllPrivateChats
from database.orm_query import orm_get_products


from handlers.user_private import user_private_router
from handlers.admin_private import admin_router
from database.engine import create_db, drop_db, session_maker



from common.bot_cmds_list import private
from middlewares.db import DataBaseSession
#ALLOWED_UPDATES = ['message, edit_message']
CATEGORY = []
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(user_private_router)



async def on_startup(bot):

    #await drop_db()

    await create_db()

async def on_shutdown(bot):
    print('бот лег')




async def main():
    
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())
