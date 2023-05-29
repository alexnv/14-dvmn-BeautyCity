import logging
from dotenv import load_dotenv

import datetime
from datetime import datetime

import aiosqlite
import qrcode
from datetime import date, datetime, timedelta
import calendar

import os
import common_helper_functions as chf
from typing import Dict
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

OK_PD, NOT_PD, CHOOSING, TYPING_REPLY, TYPING_CHOICE, START_ROUTES, END_ROUTES, FIO, ADRESS, PROCEDURES, \
COMMENT, END_DATE, OK_DE, NOT_DE, DELIVERY, SEL_QR, LOAD1, LOAD2, LOAD3, LOAD4, LOAD5, LOAD6, LOAD7, LOAD8, LOAD9, \
LOAD10, RCEPTIONHOUR, MASTER, REVIEW, OK_REW, NOT_REW, REW_TEXT, ADDREWIEV = range(33)

ORD0, ORD1, ORD2, ORD3, ORD4, ORD5, ORD6, ORD7, ORD8, ORD9, ORD10 = range(11)
ORD01, ORD11, ORD21, ORD31, ORD41, ORD51, ORD61, ORD71, ORD81, ORD91, ORD101 = range(11)
SDR1, SDR2, SDR3, SDR4, SDR5, SDR6, SDR7, SDR8, SDR9, SDR10, SDR11, SDR12, SDR13, SDR14, SDR15, SDR16, SDR17, SDR18, SDR19, SDR20, SDR21, SDR22, SDR23, SDR24, SDR25, SDR26, SDR27, SDR28, SDR29, SDR30, SDR31 = range(31)
DAY1, DAY2, DAY3, DAY4, DAY5, DAY6, DAY7, DAY8, DAY9, DAY10, DAY11, DAY12, DAY13, DAY14, DAY15, DAY16, DAY17, DAY18, DAY19, DAY20, DAY21, DAY22, DAY23, DAY24, DAY25, DAY26, DAY27, DAY28, DAY29, DAY30, DAY31 = range(31)
TIME1, TIME2, TIME3, TIME4, TIME5, TIME6, TIME7, TIME8 = range(8)
HR1, HR2, HR3, HR4, HR5, HR6, HR7, HR8 = range(8)
MAST1, MAST2, MAST3, MAST4, MAST5 = range(5)

DELIVERY_BY_COURIER = 0
FINAL_DATE = (1, 1, 1)
BEGIN_DATE = date(1, 1, 1)
TEXT_COMMENT = ' '
SPACE_FLOAT = 0
WEIGHT_FLOAT = 0
TEXT_ADRESS = ' '
TEXT_FIO = ' '
CHAT_ID = ' '
COUNT_MONTH = 1
SELECTDAYPROC = 0
SELECTDAYPROCFUNK = 0
SEL_MASTER = 0
PRROCEDURE_ID = 0
SEL_DAY = 0
TEXT_REW = ''
CUSTOMER = ''



reply_keyboard = [
    ["Помощь", "Записаться на прием"],
    ["Отзывы", "Контакты"],
    ["Выйти из бота"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                             resize_keyboard=True, input_field_placeholder="Выберите категорию")


async def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


async def create_connection():
    db = await aiosqlite.connect(chf.file_db)
    # cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects';")
    # if not await cursor.fetchone():
    #    return
    return db


async def close_connection(conn):
    await conn.close()


async def add_event(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13):  # Вставляем данные в таблицу
    event_ = (None, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13)
    async with aiosqlite.connect(chf.user_db) as db:
        await db.execute('INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', event_)
        await db.commit()


async def creat_qr(text_qr, name_file):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
    qr.add_data(text_qr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(name_file)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(chf.text_start, parse_mode="html", reply_markup=markup)
    return CHOOSING


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global CHAT_ID, ORD1, ORD2, ORD3, ORD4, ORD5, ORD6, ORD7, ORD8, ORD9, ORD10, CUSTOMER,\
        ORD11, ORD21, ORD31, ORD41, ORD51, ORD61, ORD71, ORD81, ORD91, ORD101, SDR1,\
        SDR2, SDR3, SDR4, SDR5, SDR6, SDR7, SDR8, SDR9, SDR10, SDR11, SDR12, SDR13, SDR14, \
        SDR15, SDR16, SDR17, SDR18, SDR19, SDR20, SDR21, SDR22, SDR23, SDR24, SDR25, SDR26, \
        SDR27, SDR28, SDR29, SDR30, SDR31, DAY1, DAY2, DAY3, DAY4, DAY5, DAY6, DAY7, DAY8, DAY9, \
        DAY10, DAY11, DAY12, DAY13, DAY14, DAY15, DAY16, DAY17, DAY18, DAY19, DAY20, DAY21, DAY22, \
        DAY23, DAY24, DAY25, DAY26, DAY27, DAY28, DAY29, DAY30, DAY31, TIME1, TIME2, TIME3, TIME4, TIME5, \
        TIME6, TIME7, TIME8, HR1, HR2, HR3, HR4, HR5, HR6, HR7, HR8, MAST1, MAST2, MAST3, MAST4, MAST5, CHAT_ID

    """Ask the user for info about the selected predefined choice."""
    """Запросите у пользователя информацию о выбранном предопределенном выборе."""
    text = update.message.text
    context.user_data["choice"] = text
    if text == 'Помощь':
        await update.message.reply_text(chf.text_help, parse_mode="html")
        return CHOOSING  # TYPING_REPLY

    if text == 'Записаться на прием':
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=str(OK_PD)),
                InlineKeyboardButton("Нет", callback_data=str(NOT_PD)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = "Записываясь на прием вы соглашаетесь на обработку персональных данных. \n <b>" \
               "Я согласен[на] на обработку персональных данных.</b>"
        await update.message.reply_text(text=text, parse_mode="html", reply_markup=reply_markup)
        return START_ROUTES


    if text == 'Отзывы':  # гламур
        conn = await create_connection()
        res = await conn.execute('SELECT * FROM appadmin_Feedback')
        list_ord = await res.fetchall()
        await close_connection(conn)
        text = ''
        for ord in list_ord:
            text = text + f'\nМастер {ord[2]}\nОтзыв клиента {ord[1]}\n{ord[0]}\n'

        query = update.callback_query
        query = update.message
        await query.reply_text(text=text, parse_mode="html")

        CHAT_ID = query.chat.id
        conn = await create_connection()
        res1 = await conn.execute('SELECT * FROM appadmin_customer WHERE CHAT_ID == CHAT_ID')
        list_ord = await res1.fetchall()
        await close_connection(conn)

        if len(list_ord) < 1:
            text = 'Вы не являетесь зарегистрированным ппользователем поэтому не можете оставить отзыв'
            await query.reply_text(text=text, parse_mode="html")
            return CHOOSING
        else:
            CUSTOMER = list_ord[0][1]
            keyboard = [
                [
                    InlineKeyboardButton("Да", callback_data=str(OK_REW)),
                    InlineKeyboardButton("Нет", callback_data=str(NOT_REW)),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            text = "Хотите оставить отзыв?"
            await update.message.reply_text(text=text, parse_mode="html", reply_markup=reply_markup)
            return REVIEW


async def ok_rew(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global CHAT_ID
    query = update.callback_query
    await query.answer()
    text = "Введите текст отзыва"
    await query.edit_message_text(text=text, parse_mode="html")
    return REW_TEXT

async def mastername(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global TEXT_FIO, CHAT_ID, TEXT_REW
    TEXT_REW = update.message.text
    query = update.message
    text = "Введите имя мастера "
    await query.reply_text(text=text, parse_mode="html")
    return ADDREWIEV # ADRESS


async def addrew(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global TEXT_FIO, CHAT_ID, TEXT_REW, CUSTOMER
    namemaster = update.message.text

    event_ = (TEXT_REW, CUSTOMER, namemaster)
    async with aiosqlite.connect(chf.file_db) as db:
        await db.execute('INSERT INTO appadmin_Feedback VALUES (?, ?, ?)', event_)
        await db.commit()
    text = "Ваш отзыв записан"
    query = update.message
    await query.reply_text(text=text, parse_mode="html")
    return CHOOSING




async def not_rew(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Хорошо, в следующий раз "
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=text, parse_mode="html")
    return CHOOSING


async def selectday():
    global DAY1, DAY2, DAY3, DAY4, DAY5, DAY6, DAY7, DAY8, DAY9, DAY10, DAY11, DAY12, DAY13, DAY14, DAY15, DAY16, DAY17, DAY18, DAY19, DAY20, DAY21, DAY22, DAY23, DAY24, DAY25, DAY26, DAY27, DAY28, DAY29, DAY30, DAY31
    keyboard = [
        [
            InlineKeyboardButton("  1 ", callback_data=str(DAY1)),
            InlineKeyboardButton("  2 ", callback_data=str(DAY2)),
            InlineKeyboardButton("  3 ", callback_data=str(DAY3)),
            InlineKeyboardButton("  4 ", callback_data=str(DAY4)),
            InlineKeyboardButton("  5 ", callback_data=str(DAY5)),
            InlineKeyboardButton("  6 ", callback_data=str(DAY6)),
            InlineKeyboardButton("  7 ", callback_data=str(DAY7)),
            InlineKeyboardButton("  8 ", callback_data=str(DAY8)),
        ],
        [
            InlineKeyboardButton("  9 ", callback_data=str(DAY9)),
            InlineKeyboardButton(" 10 ", callback_data=str(DAY10)),
            InlineKeyboardButton(" 11 ", callback_data=str(DAY11)),
            InlineKeyboardButton(" 12 ", callback_data=str(DAY12)),
            InlineKeyboardButton(" 13 ", callback_data=str(DAY13)),
            InlineKeyboardButton(" 14 ", callback_data=str(DAY14)),
            InlineKeyboardButton(" 15 ", callback_data=str(DAY15)),
            InlineKeyboardButton(" 16 ", callback_data=str(DAY16)),
        ],
        [
            InlineKeyboardButton(" 17 ", callback_data=str(DAY17)),
            InlineKeyboardButton(" 18 ", callback_data=str(DAY18)),
            InlineKeyboardButton(" 19 ", callback_data=str(DAY19)),
            InlineKeyboardButton(" 20 ", callback_data=str(DAY20)),
            InlineKeyboardButton(" 21 ", callback_data=str(DAY21)),
            InlineKeyboardButton(" 22 ", callback_data=str(DAY22)),
            InlineKeyboardButton(" 23 ", callback_data=str(DAY23)),
            InlineKeyboardButton(" 24 ", callback_data=str(DAY24)),
        ],
        [
            InlineKeyboardButton(" 25 ", callback_data=str(DAY25)),
            InlineKeyboardButton(" 26 ", callback_data=str(DAY26)),
            InlineKeyboardButton(" 27 ", callback_data=str(DAY27)),
            InlineKeyboardButton(" 28 ", callback_data=str(DAY28)),
            InlineKeyboardButton(" 29 ", callback_data=str(DAY29)),
            InlineKeyboardButton(" 30 ", callback_data=str(DAY30)),
            InlineKeyboardButton(" 31 ", callback_data=str(DAY31)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


async def choosetime():
    global TIME1, TIME2, TIME3, TIME4, TIME5, TIME6, TIME7, TIME8
    keyboard = [
        [
            InlineKeyboardButton(" 8.00 - 9.00 ", callback_data=str(TIME1)),
            InlineKeyboardButton(" 9.00 - 10.00 ", callback_data=str(TIME2)),
            InlineKeyboardButton(" 10.00 - 11.00 ", callback_data=str(TIME3)),
            InlineKeyboardButton(" 11.00 - 12.00 ", callback_data=str(TIME4)),
        ],
        [
            InlineKeyboardButton(" 13.00 - 14.00 ", callback_data=str(TIME5)),
            InlineKeyboardButton(" 14.00 - 15.00 ", callback_data=str(TIME6)),
            InlineKeyboardButton(" 15.00 - 16.00 ", callback_data=str(TIME7)),
            InlineKeyboardButton(" 17.00 - 18.00 ", callback_data=str(TIME8)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


async def sd1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR1, HR1, TIME1, SEL_DAY
    SEL_DAY = 1
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)

    return RCEPTIONHOUR


async def sd2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR2, SEL_DAY
    SEL_DAY = 2
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)

    return RCEPTIONHOUR


async def sd3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR3, SEL_DAY
    SEL_DAY = 3
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)

    return RCEPTIONHOUR


async def sd4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR4, SEL_DAY
    SEL_DAY = 4
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)

    return RCEPTIONHOUR


async def sd5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR5, SEL_DAY
    SEL_DAY = 5
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR5
    return RCEPTIONHOUR


async def sd6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR6, SEL_DAY
    SEL_DAY = 6
    reply_markup = await choosetime()
    text = "Выберите время визита"

    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR6
    return RCEPTIONHOUR


async def sd7(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR7, SEL_DAY
    SEL_DAY = 7
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR7
    return RCEPTIONHOUR


async def sd8(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR8, SEL_DAY
    SEL_DAY = 8
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR8
    return RCEPTIONHOUR


async def sd9(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR9, SEL_DAY
    SEL_DAY = 9
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR9
    return RCEPTIONHOUR


async def sd10(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR10, SEL_DAY
    SEL_DAY = 10
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR10
    return RCEPTIONHOUR


async def sd11(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR11, SEL_DAY
    SEL_DAY = 11
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR11
    return RCEPTIONHOUR


async def sd12(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR12, SEL_DAY
    SEL_DAY = 12
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR12
    return RCEPTIONHOUR


async def sd13(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR13, SEL_DAY
    SEL_DAY = 13
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR13
    return RCEPTIONHOUR


async def sd14(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR14, SEL_DAY
    SEL_DAY = 14
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR14
    return RCEPTIONHOUR


async def sd15(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR15, SEL_DAY
    SEL_DAY = 15
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR15
    return RCEPTIONHOUR


async def sd16(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR16, SEL_DAY
    SEL_DAY = 16
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR16
    return RCEPTIONHOUR


async def sd17(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR17, SEL_DAY
    SEL_DAY = 17
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR17
    return RCEPTIONHOUR


async def sd18(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR18, SEL_DAY
    SEL_DAY = 18
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR18
    return RCEPTIONHOUR


async def sd19(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR19, SEL_DAY
    SEL_DAY = 19
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR19
    return RCEPTIONHOUR


async def sd20(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR20, SEL_DAY
    SEL_DAY = 20
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR20
    return RCEPTIONHOUR


async def sd21(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR21, SEL_DAY
    SEL_DAY = 21
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR21
    return RCEPTIONHOUR


async def sd22(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR22, SEL_DAY
    SEL_DAY = 22
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR22
    return RCEPTIONHOUR


async def sd23(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR23, SEL_DAY
    SEL_DAY = 23
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR23
    return RCEPTIONHOUR


async def sd24(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR24, SEL_DAY
    SEL_DAY = 24
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR24
    return RCEPTIONHOUR


async def sd25(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR25, SEL_DAY
    SEL_DAY = 25
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR25
    return RCEPTIONHOUR


async def sd26(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR26, SEL_DAY
    SEL_DAY = 26
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR26
    return RCEPTIONHOUR


async def sd27(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR27, SEL_DAY
    SEL_DAY = 27
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR27
    return RCEPTIONHOUR


async def sd28(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR28, SEL_DAY
    SEL_DAY = 28
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR28
    return RCEPTIONHOUR


async def sd29(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR29, SEL_DAY
    SEL_DAY = 29
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR29
    return RCEPTIONHOUR


async def sd30(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR30, SEL_DAY
    SEL_DAY = 30
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR30
    return RCEPTIONHOUR


async def sd31(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global SELECTDAYPROC, SDR31, SEL_DAY
    SEL_DAY = 31
    reply_markup = await choosetime()
    text = "Выберите время визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    SELECTDAYPROC = SDR31
    return RCEPTIONHOUR


async def selectmaster():
    global MAST1, MAST2, MAST3, MAST4, MAST5
    conn = await create_connection()
    res = await conn.execute('SELECT * FROM appadmin_employee')
    list_ord = await res.fetchall()
    await close_connection(conn)
    keyboard = []

    n = 1
    for order in list_ord:
        if n == 1:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1],
                                       callback_data=str(MAST1))
        if n == 2:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1],
                                       callback_data=str(MAST2))
        if n == 3:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1],
                                       callback_data=str(MAST3))
        if n == 4:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1],
                                       callback_data=str(MAST4))
        if n == 5:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1],
                                       callback_data=str(MAST5))
        keyboard.insert(0, [btn])
        n = n + 1

    reply_markup = InlineKeyboardMarkup(keyboard)

    if len(list_ord) == 0:

        return CHOOSING

    return reply_markup


async def hrr1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # выбор часа
    global SELECTDAYPROC, SEL_HOUR
    SEL_HOUR = ' 8.00 - 9.00'
    text = 'Выберите Мастера'
    reply_markup = await selectmaster()
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)

    return MASTER


async def hrr2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # выбор часа
    global SELECTDAYPROC, SEL_HOUR
    SEL_HOUR = ' 9.00 - 10.00'
    text = 'Выберите Мастера'
    reply_markup = await selectmaster()
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return MASTER


async def hrr3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # выбор часа
    global SELECTDAYPROC, SEL_HOUR
    SEL_HOUR = ' 10.00 - 11.00'
    text = 'Выберите Мастера'
    reply_markup = await selectmaster()
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return MASTER


async def hrr4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # выбор часа
    global SELECTDAYPROC, SEL_HOUR
    SEL_HOUR = ' 11.00 - 12.00'
    text = 'Выберите Мастера'
    reply_markup = await selectmaster()
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return MASTER


async def hrr5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # выбор часа
    global SELECTDAYPROC, SEL_HOUR
    SEL_HOUR = ' 13.00 - 14.00'
    text = 'Выберите Мастера'
    reply_markup = await selectmaster()
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return MASTER   #  изменить


async def hrr6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # выбор часа
    global SELECTDAYPROC, SEL_HOUR
    SEL_HOUR = ' 14.00 - 15.00'
    text = 'Выберите Мастера'
    reply_markup = await selectmaster()
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return MASTER   #  изменить


async def hrr7(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # выбор часа
    global SELECTDAYPROC, SEL_HOUR
    SEL_HOUR = ' 15.00 - 16.00'
    text = 'Выберите Мастера'
    reply_markup = await selectmaster()
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return MASTER


async def hrr8(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # выбор часа
    global SELECTDAYPROC, SEL_HOUR
    SEL_HOUR = ' 17.00 - 18.00'
    text = 'Выберите Мастера'
    reply_markup = await selectmaster()
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return MASTER


async def qr1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 1
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 2
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 3
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 4
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 5
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 6
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr7(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 7
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr8(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 8
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr9(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 9
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK


async def qr10(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global PRROCEDURE_ID
    PRROCEDURE_ID = 10
    reply_markup = await selectday()
    text = "Выберите дату визита"
    query = update.callback_query
    await query.edit_message_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return SELECTDAYPROCFUNK



async def status_pd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global OK_PD, NOT_PD
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(OK_PD)),
            InlineKeyboardButton("Нет", callback_data=str(NOT_PD)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Создавая заказ вы соглашаетесь на обработку персональных данных. \n <b>" \
           "Я согласен на обработку персональных данных.</b>"
    await update.message.reply_text(text=text, parse_mode="html", reply_markup=reply_markup)
    return START_ROUTES


async def ok_pd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    text = "Как к Вам обращаться?\n <b>" \
           "Введите Ваше Имя [Отчество]</b>"
    await query.edit_message_text(text=text, parse_mode="html")

    return FIO


async def fio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global TEXT_FIO, CHAT_ID, BEGIN_DATE
    TEXT_FIO = update.message.text
    CHAT_ID = update.message.chat.id
    BEGIN_DATE = update.message.date

    query = update.message
    text = " <b> Введите Ваш телефон для связи</b> "
    await query.reply_text(text=text, parse_mode="html")
    return ADRESS


async def adress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global TEXT_ADRESS, ORD1, ORD2, ORD3, ORD4, ORD5, ORD6, ORD7, ORD8, ORD9, ORD10, TEXT_FIO, CHAT_ID, BEGIN_DATE
    TEXT_ADRESS = update.message.text
    # вносим данные о пользователе
    conn = await create_connection()
    res = await conn.execute('SELECT * FROM appadmin_customer WHERE CHAT_ID == CHAT_ID')
    list_ord = await res.fetchall()
    await close_connection(conn)
    if len(list_ord) < 1:
        event_ = (None, TEXT_FIO, TEXT_ADRESS, CHAT_ID)
        async with aiosqlite.connect(chf.file_db) as db:
            await db.execute('INSERT INTO appadmin_customer VALUES (?, ?, ?, ?)', event_)
            await db.commit()

    query = update.message
    conn = await create_connection()
    res = await conn.execute('SELECT * FROM appadmin_serivice')
    list_ord = await res.fetchall()
    await close_connection(conn)
    keyboard = []

    n = 1
    for order in list_ord:
        if n == 1:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD1))
        if n == 2:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD2))
        if n == 3:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD3))
        if n == 4:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD4))
        if n == 5:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD5))
        if n == 6:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD6))
        if n == 7:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD7))
        if n == 8:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD8))
        if n == 9:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD9))
        if n == 10:

            btn = InlineKeyboardButton(str(order[0]) + '  ' + order[1] + '  ' + str(order[2]) + '  руб.',
                                       callback_data=str(ORD10))

        keyboard.insert(0, [btn])
        n = n + 1

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Выберите процедуру"
    if len(list_ord) == 0:
        text = 'На ближайший месяц все мастера заняты'
        await update.message.reply_text(text=text, parse_mode="html")
        return CHOOSING

    text = "Выберите необходимую процедуру"

    await update.message.reply_text(text=text, parse_mode="html", reply_markup=reply_markup)

    return SEL_QR  # PROCEDURES


async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global TEXT_COMMENT
    TEXT_COMMENT = update.message.text
    query = update.message
    text = " <b>  Введите количество месяцев хранения (максимум 12).</b>"
    await query.reply_text(text=text, parse_mode="html")
    return END_DATE


async def enddate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global FINAL_DATE, BEGIN_DATE
    try:
        COUNT_MONTH = int(update.message.text.replace(' ', ''))
        if COUNT_MONTH > 12:
            COUNT_MONTH = 12
    except:
        COUNT_MONTH = 12
    FINAL_DATE = await add_months(BEGIN_DATE, COUNT_MONTH)
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(OK_DE)),
            InlineKeyboardButton("Нет", callback_data=str(NOT_DE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = " <b> Я привезу свои вещи сам.</b>"
    await update.message.reply_text(text=text, parse_mode="html", reply_markup=reply_markup)
    # query = update.callback_query
    # await query.answer()
    return DELIVERY

async def addvisit():
    global SEL_MASTER, TEXT_FIO, TEXT_ADRESS, PRROCEDURE_ID, SEL_DAY, SEL_HOUR, CHAT_ID, BEGIN_DATE
    conn = await create_connection()
    res = await conn.execute(f'SELECT * FROM appadmin_schedule WHERE employee_id == {SEL_MASTER}')
    list_ord = await res.fetchall()
    await close_connection(conn)
    hournew = int(SEL_HOUR[:SEL_HOUR.find('.00 -')])
    deynew = int(SEL_DAY)
    if len(list_ord) > 0:
        for ord in list_ord:
            ordday = datetime.fromisoformat(ord[2]).day
            ordhour = datetime.fromisoformat(ord[2]).hour
            if ordday == deynew and ordhour == hournew:
                nameproc = '1'
                namespec = '1'
                return nameproc, namespec

    # добавить строку
    dt = datetime.now()
    monthnew = dt.month
    if deynew <= dt.day:
        monthnew = monthnew + 1
        if monthnew == 13:
            monthnew = 1

    datenew = datetime(dt.year, monthnew, deynew, hournew)

    event_ = (None, datetime.now(), datenew, None, None, 500, None, None, PRROCEDURE_ID, SEL_MASTER)
    async with aiosqlite.connect(chf.file_db) as db:
        await db.execute('INSERT INTO appadmin_schedule VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', event_)
        await db.commit()


    conn = await create_connection()
    res = await conn.execute(f'SELECT * FROM appadmin_employee WHERE id == {SEL_MASTER}')
    list_ord = await res.fetchall()
    await close_connection(conn)
    namespec = list_ord[0][1]

    conn = await create_connection()
    res = await conn.execute(f'SELECT * FROM appadmin_serivice WHERE id == {PRROCEDURE_ID}')
    list_ord = await res.fetchall()
    await close_connection(conn)
    nameproc = list_ord[0][1]

    return nameproc, namespec


async def m1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MAST1, SEL_MASTER, TEXT_FIO, TEXT_ADRESS, PRROCEDURE_ID, SEL_DAY, SEL_HOUR, CHAT_ID, BEGIN_DATE
    SEL_MASTER = 1
    nameproc, namespec = await addvisit()

    text = 'Ваш визит внесен в график: \n\n' \
           f'ИМЯ:  {TEXT_FIO} \n' \
           f'Телефон: {TEXT_ADRESS} \n' \
           f'Процедура {nameproc} \n' \
           f'Специалист {namespec} \n' \
           f'Число и время: {SEL_DAY}   {SEL_HOUR} \n\n' \
           '<b>Вам придет напоминание о визите за 1 день и за час вам позвонят на указанный номер </b>'
    if nameproc == '1' and namespec == '1':
        text = 'Это время занято'

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=text, parse_mode="html")

    return CHOOSING


async def m2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MAST2, SEL_MASTER, TEXT_FIO, TEXT_ADRESS, PRROCEDURE_ID, SEL_DAY, SEL_HOUR
    SEL_MASTER = 2
    nameproc, namespec = await addvisit()

    text = 'Ваш визит внесен в график: \n\n' \
           f'ИМЯ:  {TEXT_FIO} \n' \
           f'Телефон: {TEXT_ADRESS} \n' \
           f'Процедура {nameproc} \n' \
           f'Специалист {namespec} \n' \
           f'Число и время: {SEL_DAY}   {SEL_HOUR} \n\n' \
           '<b>Вам придет напоминание о визите за 1 день и за час вам позвонят на указанный номер </b>'


    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=text, parse_mode="html")

    return CHOOSING



async def m3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MAST3, SEL_MASTER, TEXT_FIO, TEXT_ADRESS, PRROCEDURE_ID, SEL_DAY, SEL_HOUR
    SEL_MASTER = 3
    nameproc, namespec = await addvisit()

    text = 'Ваш визит внесен в график: \n\n' \
           f'ИМЯ:  {TEXT_FIO} \n' \
           f'Телефон: {TEXT_ADRESS} \n' \
           f'Процедура {nameproc} \n' \
           f'Специалист {namespec} \n' \
           f'Число и время: {SEL_DAY}   {SEL_HOUR} \n\n' \
           '<b>Вам придет напоминание о визите за 1 день и за час вам позвонят на указанный номер </b>'


    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=text, parse_mode="html")

    return CHOOSING


async def m4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MAST4, SEL_MASTER, TEXT_FIO, TEXT_ADRESS, PRROCEDURE_ID, SEL_DAY, SEL_HOUR
    SEL_MASTER = 4

    nameproc, namespec = await addvisit()

    text = 'Ваш визит внесен в график: \n\n' \
           f'ИМЯ:  {TEXT_FIO} \n' \
           f'Телефон: {TEXT_ADRESS} \n' \
           f'Процедура {nameproc} \n' \
           f'Специалист {namespec} \n' \
           f'Число и время: {SEL_DAY}   {SEL_HOUR} \n\n' \
           '<b>Вам придет напоминание о визите за 1 день и за час вам позвонят на указанный номер </b>'


    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=text, parse_mode="html")

    return CHOOSING


async def m5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global MAST5, SEL_MASTER, TEXT_FIO, TEXT_ADRESS, PRROCEDURE_ID, SEL_DAY, SEL_HOUR
    SEL_MASTER = 5

    nameproc, namespec = await addvisit()

    text = 'Ваш визит внесен в график: \n\n' \
           f'ИМЯ:  {TEXT_FIO} \n' \
           f'Телефон: {TEXT_ADRESS} \n' \
           f'Процедура {nameproc} \n' \
           f'Специалист {namespec} \n' \
           f'Число и время: {SEL_DAY}   {SEL_HOUR} \n\n' \
           '<b>Вам придет напоминание о визите за 1 день и за час вам позвонят на указанный номер </b>'

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=text, parse_mode="html")

    return CHOOSING



async def not_pd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    text = "Без вашего согласия мы не можем оказать услугу\n <b>" \
           "Попробуйте переосмыслить свою позицию</b>"
    await query.edit_message_text(text=text, parse_mode="html")
    return CHOOSING


async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    """Запросите у пользователя описание пользовательской категории."""

    await update.message.reply_text(chf.text_Contacts)
    return TYPING_CHOICE


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    """Сохранить информацию, предоставленную пользователем, и запросить следующую категорию."""

    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Пожалуйста, внимательнее. Скорее всего неправомерный ввод или двойной клик на меню",
        reply_markup=markup,
    )
    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    """Показать собранную информацию и завершить разговор."""

    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text("Работа бота завершена. Чтобы возобновить наберите /start", reply_markup=ReplyKeyboardRemove(),)
    user_data.clear()
    return ConversationHandler.END


def main() -> None:

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    load_dotenv()
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    application = Application.builder().token(telegram_token).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    # Добавить обработчик диалога с состояниями ВЫБОР,    ВВОД ВЫБОРА  и   ВВОД ОТВЕТА

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(ok_pd, pattern="^" + str(OK_PD) + "$"),
                CallbackQueryHandler(not_pd, pattern="^" + str(NOT_PD) + "$")
            ],
            REVIEW: [
                CallbackQueryHandler(ok_rew, pattern="^" + str(OK_REW) + "$"),
                CallbackQueryHandler(not_rew, pattern="^" + str(NOT_REW) + "$")
            ],
            MASTER: [
                CallbackQueryHandler(m1, pattern="^" + str(MAST1) + "$"),
                CallbackQueryHandler(m2, pattern="^" + str(MAST2) + "$"),
                CallbackQueryHandler(m3, pattern="^" + str(MAST3) + "$"),
                CallbackQueryHandler(m4, pattern="^" + str(MAST4) + "$"),
                CallbackQueryHandler(m5, pattern="^" + str(MAST5) + "$"),
            ],
            CHOOSING: [MessageHandler(filters.Regex("^(Помощь|Записаться на прием|Отзывы)$"), regular_choice),
                       MessageHandler(filters.Regex("^Контакты$"), custom_choice), ],
            TYPING_CHOICE: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выйти из бота$")), regular_choice)],
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выйти из бота$")), received_information, )],
            FIO: [MessageHandler(filters.TEXT, fio)],
            REW_TEXT: [MessageHandler(filters.TEXT, mastername)],
            ADRESS: [MessageHandler(filters.TEXT, adress)],
            ADDREWIEV: [MessageHandler(filters.TEXT, addrew)],
            COMMENT: [MessageHandler(filters.TEXT, comment)],
            END_DATE: [MessageHandler(filters.TEXT, enddate)],
            RCEPTIONHOUR: [
                CallbackQueryHandler(hrr1, pattern="^" + str(HR1) + "$"),
                CallbackQueryHandler(hrr2, pattern="^" + str(HR2) + "$"),
                CallbackQueryHandler(hrr3, pattern="^" + str(HR3) + "$"),
                CallbackQueryHandler(hrr4, pattern="^" + str(HR4) + "$"),
                CallbackQueryHandler(hrr5, pattern="^" + str(HR5) + "$"),
                CallbackQueryHandler(hrr6, pattern="^" + str(HR6) + "$"),
                CallbackQueryHandler(hrr7, pattern="^" + str(HR7) + "$"),
                CallbackQueryHandler(hrr8, pattern="^" + str(HR8) + "$")
            ],
            SEL_QR: [
                CallbackQueryHandler(qr1, pattern="^" + str(ORD1) + "$"),
                CallbackQueryHandler(qr2, pattern="^" + str(ORD2) + "$"),
                CallbackQueryHandler(qr3, pattern="^" + str(ORD3) + "$"),
                CallbackQueryHandler(qr4, pattern="^" + str(ORD4) + "$"),
                CallbackQueryHandler(qr5, pattern="^" + str(ORD5) + "$"),
                CallbackQueryHandler(qr6, pattern="^" + str(ORD6) + "$"),
                CallbackQueryHandler(qr7, pattern="^" + str(ORD7) + "$"),
                CallbackQueryHandler(qr8, pattern="^" + str(ORD8) + "$"),
                CallbackQueryHandler(qr9, pattern="^" + str(ORD9) + "$"),
                CallbackQueryHandler(qr10, pattern="^" + str(ORD10) + "$")
            ],
            SELECTDAYPROCFUNK: [
                CallbackQueryHandler(sd1, pattern="^" + str(SDR1) + "$"),
                CallbackQueryHandler(sd2, pattern="^" + str(SDR2) + "$"),
                CallbackQueryHandler(sd3, pattern="^" + str(SDR3) + "$"),
                CallbackQueryHandler(sd4, pattern="^" + str(SDR4) + "$"),
                CallbackQueryHandler(sd5, pattern="^" + str(SDR5) + "$"),
                CallbackQueryHandler(sd6, pattern="^" + str(SDR6) + "$"),
                CallbackQueryHandler(sd7, pattern="^" + str(SDR7) + "$"),
                CallbackQueryHandler(sd8, pattern="^" + str(SDR8) + "$"),
                CallbackQueryHandler(sd9, pattern="^" + str(SDR9) + "$"),
                CallbackQueryHandler(sd10, pattern="^" + str(SDR10) + "$"),
                CallbackQueryHandler(sd11, pattern="^" + str(SDR11) + "$"),
                CallbackQueryHandler(sd12, pattern="^" + str(SDR12) + "$"),
                CallbackQueryHandler(sd13, pattern="^" + str(SDR13) + "$"),
                CallbackQueryHandler(sd14, pattern="^" + str(SDR14) + "$"),
                CallbackQueryHandler(sd15, pattern="^" + str(SDR15) + "$"),
                CallbackQueryHandler(sd16, pattern="^" + str(SDR16) + "$"),
                CallbackQueryHandler(sd17, pattern="^" + str(SDR17) + "$"),
                CallbackQueryHandler(sd18, pattern="^" + str(SDR18) + "$"),
                CallbackQueryHandler(sd19, pattern="^" + str(SDR19) + "$"),
                CallbackQueryHandler(sd20, pattern="^" + str(SDR20) + "$"),
                CallbackQueryHandler(sd21, pattern="^" + str(SDR21) + "$"),
                CallbackQueryHandler(sd22, pattern="^" + str(SDR22) + "$"),
                CallbackQueryHandler(sd23, pattern="^" + str(SDR23) + "$"),
                CallbackQueryHandler(sd24, pattern="^" + str(SDR24) + "$"),
                CallbackQueryHandler(sd25, pattern="^" + str(SDR25) + "$"),
                CallbackQueryHandler(sd26, pattern="^" + str(SDR26) + "$"),
                CallbackQueryHandler(sd27, pattern="^" + str(SDR27) + "$"),
                CallbackQueryHandler(sd28, pattern="^" + str(SDR28) + "$"),
                CallbackQueryHandler(sd29, pattern="^" + str(SDR29) + "$"),
                CallbackQueryHandler(sd20, pattern="^" + str(SDR30) + "$"),
                CallbackQueryHandler(sd31, pattern="^" + str(SDR31) + "$")
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Выйти из бота$"), done)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()