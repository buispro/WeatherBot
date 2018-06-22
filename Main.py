import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import constants
import time
import datetime

bot = telepot.Bot(constants.Token)


def handle(msg):
    if telepot.flavor(msg) == "chat":
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            logic(msg['text'], chat_id)
    elif telepot.flavor(msg) == "callback_query":
        callback_id, chat_id, data, msg_id = msg['id'], msg['from']['id'], msg['data'], msg["message"]["message_id"]
        if data == "turn":
            constants.status[chat_id] = (constants.status[chat_id] + 1) % 2
            if constants.status[chat_id] == 0:
                constants.btn_text = "Выключено"
            else:
                constants.btn_text = "Включено"
            bot.answerCallbackQuery(callback_id, "Режим изменён")
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[{"text": "Выбрать время", "callback_data": "time"},
                                                              {"text": constants.btn_text, "callback_data": "turn"}]])
            text = "Вы в главном меню."
        elif data == "time":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[{"text": "Главное меню", "callback_data": "main_menu"}],
                                                             [{"text": "Добавить время", "callback_data": "add"},
                                                              {"text": "Удалить время", "callback_data": "change"}]])
            text = "Выберите действие:"
        elif data == "main_menu":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[{"text": "Выбрать время", "callback_data": "time"},
                                                              {"text": constants.btn_text, "callback_data": "turn"}]])
            text = "Вы в главном меню."
        elif data == "add":
            keyboard = InlineKeyboardMarkup()
            text = "Введите время в формате: чч:мм"
            constants.add_flag = True

        elif data == "change":
            btn_time = []
            fi = []
            i = 0
            for time in constants.times[chat_id]:
                i += 1
                fi.append({"text": time, "callback_data": time})
                if i % 3 == 0:
                    btn_time.append(fi)
                    fi = []
            if fi:
                btn_time.append(fi)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[{"text": "Назад", "callback_data": "time"}]] + btn_time)
            text = "Выберите время, которое хотите удалить."
        else:
            constants.times[chat_id].remove(data)
            btn_time = []
            fi = []
            i = 0
            for time in constants.times[chat_id]:
                i += 1
                fi.append({"text": time, "callback_data": time})
                if i % 3 == 0:
                    btn_time.append(fi)
                    fi = []
            if fi:
                btn_time.append(fi)
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[{"text": "Главное меню", "callback_data": "time"}]] + btn_time)
            text = "Выберите время, которое хотите удалить."
        bot.editMessageText((chat_id, msg_id), text, reply_markup=keyboard)

def logic(text, chat_id):
    if text == "/start":
        if not chat_id in constants.status:
            constants.status[chat_id] = 1
        if not chat_id in constants.times:
            constants.times[chat_id] = []
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[{"text": "Выбрать время", "callback_data": "time"},
                                                          {"text": constants.btn_text, "callback_data": "turn"}]])
        text = "Привет, я бот погода, и я буду отправлять тебе актуальный прогноз. Выбери действие ниже."
        bot.sendMessage(chat_id, text, reply_markup=keyboard)
    elif constants.add_flag:
        if not ":" in text:
            bot.sendMessage(chat_id, "Вы неправильно ввели дату. Нужный формат - чч:мм")
        else:
            hour, minutes = text.split(":")
            if hour.isdigit() and minutes.isdigit() and 0 <= int(hour) <= 23 and 0 <= int(hour) <= 59:
                if chat_id in constants.times:
                    constants.times[chat_id].append(text)
                else:
                    constants.times[chat_id] = []
                    constants.times[chat_id].append(text)
                print(constants.times[chat_id])
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[{"text": "Главное меню", "callback_data": "main_menu"}]])
                bot.sendMessage(chat_id, "Новое время добавленно!", reply_markup=keyboard)
            else:
                bot.sendMessage(chat_id, "Вы неправильно ввели дату. Нужный формат - чч:мм")




# Запускаем поток, который получает новые сообщения
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

while True:
    time.sleep(10)
