from aiogram import types
from ..config import cursor, conn
from ..config import dp
from .lib.psuti_lib import get_week


@dp.message_handler(commands=["week"])
async def week(message: types.Message):
    cursor = conn.cursor()
    cursor.execute("SELECT n_week FROM raspisanie")
    week_num = cursor.fetchone()
    week = await get_week(week=week_num)
    conn.commit()
    print(week)

    def rasp_week():
        for day in week.days:
            msg = ""
            msg += f"\n{day.date} <b>{day.name.upper()}</b>\n"
            for class_ in day.classes:
                msg += f"{class_.n}. {class_.time_start} — {class_.time_end} - <b>{class_.discipline}</b>\n"

                if class_.method != "":
                    msg += f"<b>Способ:</b> {class_.method}\n"
                if class_.cabinet != "None":
                    msg += f"<b>Кабинет:</b> {class_.cabinet}\n"
                if class_.professor != "":
                    msg += f"<b>Преподаватель:</b> {class_.professor}\n"
                if class_.topic != "":
                    msg += f"<b>Тема занятия:</b> {class_.topic}\n"
                if class_.source is not None:
                    msg += f"<b>Ресурс:</b> <a href='{class_.source.href}'>{class_.source.name.capitalize()}</a>\n"
                if class_.task is not None:
                    msg += f"<b>Задание:</b> <a href='{class_.task.href}'>{class_.task.name.capitalize()}</a>\n"
                msg += "\n"
            return msg

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="random_value"))
    msg = await message.reply(rasp_week(), parse_mode="HTML", disable_web_page_preview=True, reply_markup=keyboard)
    print("1")
    await msg.edit_text("HUI")

    return msg


@dp.callback_query_handler(text="random_value")
async def next_week(call: types.CallbackQuery):
    cursor = conn.cursor()
    cursor.execute("UPDATE raspisanie SET n_week=n_week+1")
    cursor.execute("SELECT n_week FROM raspisanie")
    week_nu = cursor.fetchone()
    week_num = await get_week(week=week_nu)
    conn.commit()
    print(week_num)

    return week_num
