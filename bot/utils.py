import threading
import time
from functools import partial
from typing import Union

import telebot
from telebot.types import Message, CallbackQuery
from loguru import logger
from datetime import datetime
from time import sleep

from bot.buttons import Buttons, Callbacks
from bot.db_calls import get_new_requests, get_pay_in_history, get_pay_out_history, get_request, get_user_cpu_info, \
    approve_withdrawal, last_req_id, deny_withdrawal_request
from global_vars import TOKEN, megabite_id
from bot.messages import Messages
from bot.markups import main_menu, pay_in_markup, pay_out_markup, new_withdrawal_requests, handle_withdrawal_request, \
    confirm_out, delay_time, history_inline, requests_list, deny_request

bot = telebot.TeleBot(TOKEN)

last_request = {'id': 0}

handle_request = {'r_id': '0'}


def schedule_message(chat_id: int, text: str, method, reply_markup=None):
    """
    :param chat_id: айди чата
    :param text:
    :param method:
    :param reply_markup:
    :return:
    """
    try:
        msg = bot.send_message(chat_id=chat_id,
                               text=text,
                               reply_markup=reply_markup,
                               parse_mode="html")
    except Exception as e:
        logger.error(e)
    else:
        bot.register_next_step_handler(msg, method)
        return msg


def start_bot_from_code():
    # bot.remove_webhook()
    bot.infinity_polling()


def get_info_from_message(message: Union[Message, CallbackQuery], callback_str: str = None) -> tuple[int, str, int]:
    """
        Метод для получения данных с сообщения будь-то колбека или обычного
    :param callback_str: коллбек начало которое нужно обрезать
    :param message: необходимое сообщение
    :return: айди, текст, айди сообщения
    """

    if isinstance(message, Message):
        if message.content_type != 'text':
            return message.from_user.id, message.caption, message.message_id
        else:
            return message.from_user.id, message.text, message.message_id
    else:
        return message.from_user.id, message.data[len(callback_str) - 2:], message.message.message_id


def convert_time(time):
    return datetime.utcfromtimestamp(time).strftime('%d-%m-%Y %H:%M:%S')


def message_data_handler(code: str, message: Union[Message, CallbackQuery]) -> bool:
    """
        Обработка "ловли" сообщения на код если это хендлер на сообщение,
        или если это колбек на кнопке
    """
    if isinstance(message, Message):
        return code == message.text

    else:
        return message.data.startswith(code[:code.find('_') + 1] if '_' in code else code)


@bot.message_handler(commands=["start"])
@bot.message_handler(func=partial(message_data_handler, Buttons.MAIN_MENU))
def start_bot(message: Message = None):
    if message:

        if isinstance(message, CallbackQuery):
            chat_id, text, message_id = get_info_from_message(message=message, callback_str=message.data)

        else:
            chat_id, text, message_id = get_info_from_message(message=message)

        logger.info(f'user {chat_id} started the bot')
    markup = main_menu(chat_id=chat_id)

    bot.send_message(chat_id=chat_id,
                     text=Messages.START_MESSAGE,
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def go_to_new_requests(message: Message):
    if message.text.startswith(Buttons.TX_NEW[:-4]):
        pay_out_requests(message=message)


@bot.message_handler(func=partial(message_data_handler, Buttons.TX_NEW.format(str(len(get_new_requests())))))
def pay_out_requests(message: Message):
    if message:
        chat_id = message.chat.id
        logger.info(f"{chat_id} entered Pay Out Requests")
        markup = new_withdrawal_requests(chat_id=chat_id)

        bot.send_message(chat_id=chat_id,
                         text=Messages.TO_REQUESTS.format(str(len(get_new_requests()))),
                         reply_markup=requests_list(chat_id=chat_id),
                         parse_mode='html')

        bot.send_message(chat_id=chat_id,
                         text=Messages.NEW_REQUESTS,
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(Callbacks.MODERATE_REQUEST[:-2]))
def handle_w_request(callback: CallbackQuery):
    chat_id, text, message_id = get_info_from_message(message=callback,
                                                      callback_str=Callbacks.MODERATE_REQUEST)

    bot.delete_message(chat_id=chat_id, message_id=message_id)

    if text == 'back':
        start_bot(message=callback)

    elif text.isdigit():
        handle_request['r_id'] = text
        output_request(chat_id=chat_id,
                       r_id=text)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(Callbacks.PAY_IN_HISTORY[:-2]))
def show_pay_in_history(callback: CallbackQuery):
    chat_id, text, message_id = get_info_from_message(message=callback,
                                                      callback_str=Callbacks.PAY_IN_HISTORY)
    print(text)
    logger.info(f'Entering Pay in history')

    pay_in_history = get_pay_in_history(username=text)

    try:
        bot.send_message(chat_id=chat_id,
                         text="Высылаю историю <b>пополнейний</b>.",
                         parse_mode='html')

        for tx in pay_in_history:
            tx_id = tx[0]
            email = tx[2]
            login = tx[1]
            amount = str(int(tx[5]))
            date = convert_time(int(tx[13]))
            system = tx[4]

            bot.send_message(chat_id=chat_id,
                             text=Messages.PAY_IN_HISTORY.format(
                                 str(tx_id), email, login,
                                 amount, date, system
                             ))
            sleep(0.3)
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda callback: callback.data.startswith(Callbacks.PAY_OUT_HISTORY[:-2]))
def pay_out(callback: CallbackQuery):
    chat_id, text, message_id = get_info_from_message(message=callback,
                                                      callback_str=Callbacks.PAY_OUT_HISTORY)
    pay_out_history = get_pay_out_history(username=text)

    if pay_out_history:

        try:
            bot.send_message(chat_id=chat_id,
                             text="Высылаю историю <b>выводов.</b>",
                             parse_mode='html')

            for tx in pay_out_history:
                tx_id = tx[0]
                email = tx[2]
                login = tx[1]
                amount = str(int(tx[7]))
                date = convert_time(int(tx[15]))
                system = tx[5]

                bot.send_message(chat_id=chat_id,
                                 text=Messages.PAY_OUT_HISTORY.format(
                                     str(tx_id), email, login, amount,
                                     date, system
                                 ))
                sleep(0.3)

        except Exception as e:
            print(e)
    else:
        bot.send_message(chat_id=chat_id,
                         text=Messages.NO_PAY_OUT_BEFORE,
                         parse_mode='html')


def output_request(chat_id: int, r_id: str):
    """
    :param chat_id: id of the user
    :param r_id: id of the request on db
    :return: information about the request
    """
    logger.info(f"{chat_id} is moderating request no. {r_id}")

    tx = get_request(r_id=str(r_id))

    proc_num, proc_price, ref_num, earned = get_user_cpu_info(username=tx[1])

    try:

        tx_id = tx[0]
        email = tx[2]
        login = tx[1]
        sum_out = str(int(tx[7]))
        wallet = tx[3]
        proc_amount = tx[5]
        date = convert_time(int(tx[15]))
        system = tx[5]

        schedule_message(chat_id=chat_id,
                         text=Messages.WITHDRAWAL_REQUESTS.format(
                             str(tx_id), email, login, sum_out,
                             date, wallet, proc_num, proc_price,
                             '0', '0', ref_num, earned, '0',
                         ),
                         reply_markup=history_inline(chat_id=chat_id, username=str(login)),
                         method=request_response)

        bot.send_message(chat_id=chat_id,
                         text=Messages.NEXT_ACTION,
                         reply_markup=handle_withdrawal_request(chat_id=chat_id))

    except Exception as e:
        print(e)


def request_response(message: Message):
    chat_id, text, message_id = get_info_from_message(message)
    if message.text == Buttons.APPROVE:
        schedule_message(chat_id=chat_id,
                         text=Messages.CONFIRMATION_QUESTION,
                         reply_markup=confirm_out(chat_id=chat_id),
                         method=approve_or_deny)
    elif message.text == Buttons.APPROVE_DELAYED:
        schedule_message(chat_id=chat_id,
                         text=Messages.DELAY_TIME_INPUT,
                         reply_markup=delay_time(chat_id=chat_id),
                         method=set_delay)
    elif message.text == Buttons.DENY:
        schedule_message(chat_id=message.chat.id,
                         text=Messages.DENIAL_REASON,
                         method=complete_denial,
                         reply_markup=deny_request(chat_id=message.chat.id))

    elif message.text == Buttons.MAIN_MENU:
        start_bot(message=message)
    elif message.text == Buttons.BACK:
        pay_out_requests(message=message)


def approve_or_deny(message: Message):
    if message.text == Buttons.YES:
        approve = approve_withdrawal(r_id=handle_request['r_id'])
        if approve:
            bot.send_message(chat_id=message.chat.id,
                             text=Messages.APPROVE_SUCCESS.format(handle_request['r_id']),
                             parse_mode='html')
            pay_out_requests(message=message)
        else:
            if approve:
                bot.send_message(chat_id=message.chat.id,
                                 text=Messages.APPROVE_ERROR.format(handle_request['r_id']),
                                 parse_mode='html')
                pay_out_requests(message=message)
    else:
        output_request(chat_id=message.chat.id,
                       r_id=handle_request['r_id'])


def set_delay(message: Message):
    if message.text.isdigit():
        pass
    elif message.text == Buttons.BACK:
        output_request(chat_id=message.chat.id,
                       r_id=handle_request['r_id'])
    elif message.text == Buttons.MAIN_MENU:
        start_bot(message)
    else:
        schedule_message(chat_id=message.chat.id,
                         text="Введите только цифры.",
                         method=set_delay,
                         reply_markup=delay_time(chat_id=message.chat.id))


def complete_denial(message: Message):
    if message.text == Buttons.BACK:
        output_request(chat_id=message.chat.id,
                       r_id=handle_request['r_id'])
    else:
        try:
            deny_withdrawal_request(r_id=handle_request['r_id'], description=message.text)
            bot.send_message(chat_id=message.chat.id,
                             text=Messages.DENIED_SUCCESSFULLY)
            pay_out_requests(message=message)
        except Exception as e:
            logger.error(e)


exit_signal = threading.Event()


def check_new_requests():
    last = last_req_id()
    if last > last_request['id']:
        last_request['id'] = last
        bot.send_message(chat_id=megabite_id,
                         text="❗️Появился новый запрос на вывод❗️")
    try:
        threading.Timer(30, check_new_requests)
    except KeyboardInterrupt():
        logger.error(KeyboardInterrupt)
