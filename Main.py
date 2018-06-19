import constants
import requests


def send_request(method, data):
    try:  # обрабатываем исключения
        request = requests.get(constants.URL + constants.Token + "/" + method, data=data)
    except:
        print('Error {0}'.format(method))
        return False
    if not request.status_code == 200: return False  # проверяем пришедший статус ответа
    if not request.json()['ok']: return False
    return request


def get_update():
    request = send_request("getUpdates", {"offset": constants.offset + 1})
    if request:
        for packet in request.json()['result']:
            constants.offset = packet['update_id']
            if not "text" in packet["message"]:
                print('Unknown message')
                continue
            send_message(analysis(packet["message"]["text"]), packet["message"]["chat"]["id"])


def analysis(text):
    if "Артём" in text:
        return "Что?"
    else:
        return "Я вас не понял :)"


def send_message(text, chat_id):
    message_data = {
        'chat_id': chat_id,  # куда отправляем сообщение
        'text': text,  # само сообщение для отправки
    }
    send_request("sendMessage", message_data)


while True:
    get_update()
