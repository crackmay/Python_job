from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, Filter
from database.orm_query import orm_get_products
from kbds import reply
from sqlalchemy.ext.asyncio import AsyncSession
from kbds.inline import get_callback_btns, get_inlineMix_btns
from kbds.reply import get_keyboard
user_private_router = Router()



@user_private_router.message(or_f(CommandStart(), Command('keyboard')))
async def start_cmd(message: types.Message, session: AsyncSession):
    # for product in await orm_get_products(session):
    #     list_category.append(product.category)
    # print(list_category)
    await message.answer('Тут надо добавить приветственный текст какой либо №3', reply_markup=reply.start_kb)

# @user_private_router.message(Command('keyboard'))
# async def start_cmd(message: types.Message):
#     await message.answer(reply_markup=reply.start_kb)

@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    
    await message.answer('Здесь уже подробная информация о нас')

@user_private_router.message(Command('bot_info'))
async def bot_cmd(message: types.Message):
    
    await message.answer(f'🧰Разработал бота: @Grozny_boss', reply_markup=get_inlineMix_btns(
        btns={
            "Заказать бота🤖": "https://t.me/Grozny_boss",
            "Канал📰": "https://t.me/grozny_boss_blog",
        }
    ))


# @user_private_router.message(F.text == 'Категории товаров')
# async def all_product(message: types.Message, session: AsyncSession):
#     for product in await orm_get_products(session):
#         await message.answer_photo(
#             product.image,
#             caption=f"<strong>{product.name}\
#                     </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
#             reply_markup=get_callback_btns(
#                 btns={
#                     "Удалить": f"delete_{product.id}",
#                     "Изменить": f"change_{product.id}",
#                 }
#             ),
#         )
#     await message.answer("ОК, вот список товаров ⏫")

    
# @user_private_router.message(F.text == 'Категории товаров')
# async def all_category(message: types.Message, session: AsyncSession):
#     btns = {}
#     for product in await orm_get_products(session):
#         btns.update({f"{product.category}": f"text_{product.category}"})
     
#     await message.answer('Категории товаров ⏬',  reply_markup=get_callback_btns( btns=btns ),)
    

@user_private_router.message(F.text == 'Категории товаров')
async def all_category(message: types.Message, session: AsyncSession):
    list = []
    for product in await orm_get_products(session):
        list.append(f"{product.category}")
     
    await message.answer('Категории товаров ⏬',  reply_markup=get_keyboard( *list ),)

@user_private_router.message(F.text == 'Вернуться назад')
async def back(message: types.Message, session: AsyncSession):
    list = []
    for product in await orm_get_products(session):
        list.append(f"{product.category}")
    await message.answer('Категории товаров ⏬', reply_markup=get_keyboard( *list ))    








@user_private_router.message(or_f(F.text.contains('Антиоксиданты') ))
@user_private_router.message(or_f(F.text.contains('Антистресс') ))
@user_private_router.message(or_f(F.text.contains('Детокс') ))
@user_private_router.message(or_f(F.text.contains('Для женщин') ))
@user_private_router.message(or_f(F.text.contains('Для ЖКТ') ))
@user_private_router.message(or_f(F.text.contains('Для иммунитета') ))
@user_private_router.message(or_f(F.text.contains('Для кожи, волос, ногтей') ))
@user_private_router.message(or_f(F.text.contains('Для легких') ))
@user_private_router.message(or_f(F.text.contains('Для мозга') ))
@user_private_router.message(or_f(F.text.contains('Для мужчин') ))
@user_private_router.message(or_f(F.text.contains('Для набора массы') ))
@user_private_router.message(or_f(F.text.contains('Для нервов') ))
@user_private_router.message(or_f(F.text.contains('Для печени') ))
@user_private_router.message(or_f(F.text.contains('Для почек') ))
@user_private_router.message(or_f(F.text.contains('Для спорта') ))
@user_private_router.message(or_f(F.text.contains('Для суставов') ))
@user_private_router.message(or_f(F.text.contains('Для фигуры') ))
@user_private_router.message(or_f(F.text.contains('От варикоза') ))
@user_private_router.message(or_f(F.text.contains('От давления') ))
@user_private_router.message(or_f(F.text.contains('Суперфуды') ))
@user_private_router.message(or_f(F.text.contains('Чай') ))
@user_private_router.message(or_f(F.text.contains('Специи') ))
@user_private_router.message(or_f(F.text.contains('Интимная косметика') ))
async def product_category(message: types.Message, session: AsyncSession):
    
    for product in await orm_get_products(session):
        if message.text == product.category: 
            await message.answer_photo(
                product.image,
                    caption=f"<strong>{product.name}\
                        </strong>\n{product.description}",
                reply_markup=get_inlineMix_btns(
                    btns={
                        "Товар на OZON🛒": f"{product.ozon_url}",
                        "Товар на WILDBERRIES🛒": f"{product.wildb_url}",
                    }
                ), parse_mode='HTML'
            )
    await message.answer("ОК, вот список товаров ⏫", reply_markup=get_keyboard(
            'Вернуться назад'

        ))   
 