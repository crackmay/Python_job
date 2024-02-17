from aiogram import F, Router, types, Bot
from aiogram.filters import Command, Filter, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.enums import ParseMode


from database.orm_query import (
    orm_add_product,
    orm_delete_product,
    orm_get_product,
    orm_get_products,
    orm_update_product,
)
from kbds.inline import get_callback_btns

from kbds.reply import get_keyboard

admin_list = ['885678678576','6765745','859475654', '1123517492']
class IsAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message, bot: Bot):
        for i in admin_list:
             if message.from_user.id == int(i):
                 return message.from_user.id == int(i)
                




admin_router = Router()
admin_router.message.filter(IsAdmin())
#admin_router.message.filter(IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    placeholder="Выберите действие",
    sizes=(2,),
)


@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?/n При добавлении товара есть команды: 'отмена', 'назад'.", reply_markup=ADMIN_KB)
        



@admin_router.message(F.text == "Ассортимент")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}</strong>\n{product.description}\n",
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_{product.id}",
                    "Изменить": f"change_{product.id}",
                }
            ),
            parse_mode='HTML'
        )
    await message.answer("Товары⏫")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product_callback(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer("Товар удален")
    await callback.message.answer("Товар удален!")



@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)



#Код ниже для машины состояний (FSM)
    
class AddProduct(StatesGroup):
    name = State()
    description = State()
    ozon_url = State()
    wildb_url = State()
    category = State()
    image = State()
    product_for_change = None
    texts = {
        'AddProduct:name': 'Введите название заново:',
        'AddProduct:description': 'Введите описание заново:',
        'AddProduct:ozon_url': 'Введите ccылку Ozon заново:',
        'AddProduct:wildb_url': 'Введите ссылку Wildberries заново:',
        'AddProduct:category': 'Введите категорию заново:',
        'AddProduct:image': 'Этот стейт последний, поэтому...',
    }
    

@admin_router.message(StateFilter(None) ,F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddProduct.product_for_change:
        AddProduct.product_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}")
            return
        previous = step

@admin_router.message(AddProduct.name, or_f(F.text, F.text == '.' ))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.description, or_f(F.text, F.text == '.' ))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Ссылка на OZON")
    await state.set_state(AddProduct.ozon_url)


# @admin_router.message(AddProduct.price ,or_f(F.text, F.text == '.' ))
# async def add_price(message: types.Message, state: FSMContext):
#     if message.text == '.':
#         await state.update_data(price=AddProduct.product_for_change.price)
#     else:
#         await state.update_data(price=message.text)
#     await message.answer("Ссылка на OZON")
#     await state.set_state(AddProduct.ozon_url)

@admin_router.message(AddProduct.ozon_url, or_f(F.text, F.text == '.' ))
async def add_ozon_url(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(ozon_url=AddProduct.product_for_change.ozon_url)
    else:
        await state.update_data(ozon_url=message.text)
    await message.answer("Ссылка на Wildberries")
    await state.set_state(AddProduct.wildb_url)

@admin_router.message(AddProduct.wildb_url, or_f(F.text, F.text == '.' ))
async def add_wildb_url(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(wildb_url=AddProduct.product_for_change.wildb_url)
    else:
        await state.update_data(wildb_url=message.text)
    await message.answer("Категория товара")
    await state.set_state(AddProduct.category)

@admin_router.message(AddProduct.category, or_f(F.text, F.text == '.' ))
async def add_category(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(category=AddProduct.product_for_change.category)
    else:
        await state.update_data(category=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.image, or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text and message.text == ".":
        await state.update_data(image=AddProduct.product_for_change.image)

    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddProduct.product_for_change:
            await orm_update_product(session, AddProduct.product_for_change.id, data)
        else:
            await orm_add_product(session, data)
        await message.answer("Товар добавлен/изменен", reply_markup=ADMIN_KB)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Ошибка: \n{str(e)}\nОбратись к программеру, он опять денег хочет",
            reply_markup=ADMIN_KB,
        )
        await state.clear()

    AddProduct.product_for_change = None
            
    
