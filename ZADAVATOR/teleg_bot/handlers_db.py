import os

from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

import teleg_bot.buttons
from config import TOKEN, sigma
from us_statements import Bot_Statements

bot = Bot(token=TOKEN)
router = Router()


@router.message(Command('start'))
async def start_handler(msg: Message):
    db = Session()
    user = get_user(db, msg.from_user.id)
    if user:
        await msg.answer('already_reg', reply_markup=teleg_bot.buttons.main_kb(msg.from_user.id))
    else:
        await msg.answer('welcome', reply_markup=teleg_bot.buttons.welcome_kb(msg.from_user.id))


@router.message(Command('clear'))
async def clear(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer('Cleared')


@router.message(F.text == 'reg')
async def start_reg(msg: Message, state: FSMContext):
    db = Session()
    user = get_user(db, tg_id=msg.from_user.id)
    if user:
        await msg.answer('already_reg', reply_markup=teleg_bot.buttons.main_kb(msg.from_user.id))
        return
    await state.set_state(Bot_Statements.login_wait)
    await msg.answer('login')


@router.message(Bot_Statements.login_wait)
async def reg_login(msg: Message, state: FSMContext):
    await state.update_data(login=msg.text)
    await msg.answer('password')
    await state.set_state(Bot_Statements.password_wait)


@router.message(Bot_Statements.password_wait)
async def reg_pass(msg: Message, state: FSMContext):
    login = (await state.get_data())['login']
    password = msg.text
    logged_in = check_reg(login, password)
    if logged_in:

        user = UserDTO(msg.from_user.id, login, password)
        db = Session()
        res = create_user(db, user)
        if res:
            await msg.answer('reg_success', reply_markup=teleg_bot.buttons.main_kb(msg.from_user.id))
            await state.clear()
        else:
            await msg.answer('db fail', reply_markup=teleg_bot.buttons.welcome_kb(msg.from_user.id))
            await state.clear()
    else:
        await msg.answer('reg_fail', reply_markup=teleg_bot.buttons.welcome_kb(msg.from_user.id))
        await state.clear()


@router.message(F.text == 'get_task')
async def get_task_handler(msg: Message, state: FSMContext):
    await msg.answer('wait_for_url', reply_markup=teleg_bot.buttons.main_kb(msg.from_user.id))
    await state.set_state(Bot_Statements.url_wait)


@router.message(Bot_Statements.url_wait)
async def get_url(msg: Message, state: FSMContext):
    await msg.answer('downloading_task')
    url = msg.text
    db = Session()
    user = get_user(db, msg.from_user.id)
    user.active_url = url
    update_user(db, user)
    path = get_task(user)
    photo = FSInputFile(path)
    await msg.answer_photo(photo, caption='your_task', reply_markup=teleg_bot.buttons.main_kb(msg.from_user.id))
    await state.clear()


@router.message(F.text == 'send_answer')
async def send_answer_start(msg: Message, state: FSMContext):
    tg_id = msg.from_user.id
    db = Session()
    user = get_user(db, tg_id)
    if user.active_url:
        await msg.answer('send_photo', reply_markup=teleg_bot.buttons.main_kb(msg.from_user.id))
        await state.set_state(Bot_Statements.answer_wait)
    else:
        await msg.answer('need url', reply_markup=teleg_bot.buttons.main_kb(msg.from_user.id))
        await state.set_state(Bot_Statements.url_wait)


@router.message(F.photo, Bot_Statements.answer_wait)
async def save_photo(msg: Message):
    photo = msg.photo[-1]
    tg_id = msg.from_user.id
    path = f"files/userfiles/upload{tg_id}/{photo.file_id}.jpg"
    await msg.bot.download(photo.file_id, destination=path)

    await msg.answer('photo_saved', reply_markup=teleg_bot.buttons.send_all_kb())


@router.message(F.text == "send_all")
async def send_all(msg: Message, state: FSMContext):
    db = Session()
    tg_id = msg.from_user.id
    user = get_user(db, tg_id)
    updir = f"files/userfiles/upload{tg_id}"
    paths = [(updir + '/' + str(p)) for p in os.listdir(updir)]
    send_answer(paths, user)
    user_sent_task(db, user)
    user_fs_clean_up(user)
    await msg.answer('sending_success', reply_markup=teleg_bot.buttons.main_kb(msg.from_user.id))
    await state.clear()


@router.message(F.text == 'kill_user')
async def kill_user_h(msg: Message, state: FSMContext):
    db = Session()
    user = get_user(db, msg.from_user.id)
    user_fs_clean_up(user)
    kill_user(db, user)
    await msg.answer('killed')
    await msg.answer_sticker('CAACAgIAAxkBAAEId8Zm5KckUmFW--RjW1NzJcsVVd3hegACcBIAAt6p8Et8ICHIsOd3qzYE',
                             reply_markup=teleg_bot.buttons.welcome_kb(msg.from_user.id))
    await state.clear()


@router.message(F.text == 'cancel')
async def cancel(msg: Message, state: FSMContext):
    await msg.answer('canceled', teleg_bot.buttons.main_kb(msg.from_user.id))
    await state.clear()


@router.message(F.text == 'delete_answer')
async def delete_answer_h(msg: Message):
    db = Session()
    user = get_user(db, msg.from_user.id)
    delete_answer(user)
    await msg.answer('answer_deleted')


@router.message(F.text == 'stats')
async def stats(msg: Message):
    db = Session()
    user = get_user(db, msg.from_user.id)
    delete_answer(user)
    await msg.answer('answer_deleted')