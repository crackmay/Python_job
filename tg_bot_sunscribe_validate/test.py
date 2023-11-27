import asyncio
from aiogram import Bot, Dispatcher, types
from handlers import *

import logging
import sys

bot = Bot(token='*****')
dp = Dispatcher()

async def main():
    
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')