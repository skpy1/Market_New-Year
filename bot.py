import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

bot = Bot(token='')
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()


class GetGroup(StatesGroup):
    date = State()
    time = State()
    phone = State()
    name = State()


db = sqlite3.connect("bazaDM.db")
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INT,
    userName TEXT,
    clientName TEXT,
    holidayDate TEXT,
    holidayTime TEXT,
    clientPhone TEXT
)""")

groups = types.ReplyKeyboardMarkup(resize_keyboard=True)
set_group = types.ReplyKeyboardMarkup(resize_keyboard=True)

group_one = types.KeyboardButton("Портфолио")
group_two = types.KeyboardButton("Посмотреть видео")
group_three = types.KeyboardButton("Отзывы")
group_four = types.KeyboardButton("Заказать Деда Мороза")
groups.add(group_one, group_two, group_three, group_four)


@dp.message_handler(Command('start'), state=None)
async def welcome(message):
    if message.from_user.id == message.chat.id:
        sql.execute(f"SELECT * FROM users WHERE user_id = {message.from_user.id}")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                        (message.from_user.id, message.from_user.username, None, None, None, None))
            db.commit()
    await message.answer('Добро пожаловать на офицальный телеграм бот Деда Мороза 🎅 \n\n'
                         'Здесь вы можете пригласить Деда Мороза на дом и посмотреть его портфолио ❄️.',
                         reply_markup=groups)


@dp.message_handler(content_types=['text'])
async def lalala(message):
    if message.text == 'Портфолио':
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img.png', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img1.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img2.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img3.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img4.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img5.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img6.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img7.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img8.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img9.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img10.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img11.jpg', 'rb'))
        await bot.send_photo(chat_id=message.chat.id, photo=open('/Bot/image/img12.jpg', 'rb'))

    elif message.text == 'Посмотреть видео':
        await message.answer('Секундочку, загружаю...')
        await bot.send_video(chat_id=message.chat.id,
                             video=open('/Bot/image/WhatsApp Video 2022-12-04 at 02.34.49.mp4', 'rb'))
        await bot.send_video(chat_id=message.chat.id,
                             video=open('/Bot/image/WhatsApp Video 2022-12-04 at 02.34.49 (1).mp4', 'rb'))
    elif message.text == 'Отзывы':
        await message.answer('Наши отзывы:\n https://profi.ru/profile/SchurovOE/#reviews-tab')
    elif message.text == 'Заказать Деда Мороза':
        await GetGroup.name.set()
        await message.answer("Введите Ваше имя: ")


@dp.message_handler(state=GetGroup.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy():
        await state.finish()
        sql.execute(f"UPDATE users SET clientName = '{message.text}' WHERE user_id = {message.from_user.id}")
        db.commit()
        await message.answer("Введите дату: ")
        await GetGroup.date.set()


@dp.message_handler(state=GetGroup.date)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy():
        await state.finish()
        sql.execute(f"UPDATE users SET holidayDate = '{message.text}' WHERE user_id = {message.from_user.id}")
        db.commit()
        await message.answer("Введите время: ")
        await GetGroup.time.set()


@dp.message_handler(state=GetGroup.time)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy():
        await state.finish()
        sql.execute(f"UPDATE users SET holidayTime = '{message.text}' WHERE user_id = {message.from_user.id}")
        db.commit()
        await message.answer("Введите номер телефона: ")
        await GetGroup.phone.set()


@dp.message_handler(state=GetGroup.phone)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy():
        await state.finish()
        sql.execute(f"UPDATE users SET clientPhone = '{message.text}' WHERE user_id = {message.from_user.id}")
        db.commit()
        await message.answer('Отлично! В ближайшее время я позвоню вам  и уточню детали заказа!')
        text = {'телеграм': "@" + sql.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}").fetchone()[1],
                'имя': sql.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}").fetchone()[2],
                'дата': sql.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}").fetchone()[3],
                'время': sql.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}").fetchone()[4],
                'номер телефона': sql.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}").fetchone()[5]}
        otpravka = []
        for k, v in text.items():
            otpravka.append(str(k) + ': ' + str(v) + '\n')
        await bot.send_message(chat_id='', text=''.join(otpravka))


async def on_startup(_):
    print('Бот запущен')


if __name__ == '__main__':
    # print(sql.execute("SELECT * FROM users").fetchall())
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
