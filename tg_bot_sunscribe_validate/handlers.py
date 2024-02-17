from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from app import key
from test import bot


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_name = message.from_user.username
    await message.answer(f'Салют, {user_name}! Чтобы написать пользователю, тебе нужно подписаться на канал: https://t.me/grozny_boss_blog', reply_markup=key.main)

@router.message(F.text == 'Проверить подписку')
async def valid(message: Message):
    user_id = message.from_user.id
    print(user_id)
    chat_id = '*******'
    result =  await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    new_result = str(result)
        
    res = new_result.split('>')[0]
    if res == "status=<ChatMemberStatus.LEFT: 'left'":
        await message.answer('Подпишитесь на канал: https://t.me/grozny_boss_blog', reply_markup=key.validate)

            
    else: 
        await message.answer('Вам доступен гайд "Уверенный старт на фрилансе: https://way-of-freelancing.ru/bonus')