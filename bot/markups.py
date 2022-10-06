from bot.buttons import Buttons, Callbacks
from bot.db_calls import get_new_requests
from global_vars import megabite_id
from bot.config import Keyboards
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton


def _reply_markup(chat_id: int,
                  keyboard: list = [],
                  back_: bool = False,
                  one_time: bool = False,
                  main_menu_: bool = False) -> ReplyKeyboardMarkup:
    """
    :param chat_id:
    :param keyboard:
    :param back_:
    :param one_time:
    :param main_menu_:
    :return:
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=one_time)

    if keyboard:
        for row in keyboard:
            button_row = [KeyboardButton(text=button_title) for button_title in row]
            markup.add(*button_row)

    if back_:
        markup.add(KeyboardButton(text=Buttons.BACK))

    if main_menu_:
        markup.add(KeyboardButton(text=Buttons.MAIN_MENU))

    return markup


def _inline_markup(keyboard, callback_str: str) -> InlineKeyboardMarkup:
    """
    :param keyboard:
    :param callback_str:
    :return:
    """
    markup = InlineKeyboardMarkup()

    for row in keyboard:
        button_row = [InlineKeyboardButton(text=button_title,
                                           callback_data=callback_str.format(button_title)) for button_title in row]
        markup.add(*button_row)

    return markup


def main_menu(chat_id: int) -> ReplyKeyboardMarkup():

    markup = ReplyKeyboardMarkup(resize_keyboard=True) if chat_id == megabite_id else None
    buttons = [Buttons.TX_NEW.format(str(len(get_new_requests())))]
    markup.add(*buttons)

    return markup


def requests_list(chat_id: int) -> ReplyKeyboardMarkup():
    keyboard = Keyboards.Menu.TX_LIST if chat_id == megabite_id else None
    markup = _reply_markup(keyboard=keyboard,
                           chat_id=chat_id)

    return markup


def new_withdrawal_requests(chat_id: int) -> InlineKeyboardMarkup():
    markup = InlineKeyboardMarkup(row_width=4)
    buttons = []
    new_requests = get_new_requests()

    for r in new_requests:
        buttons.append(InlineKeyboardButton(text=r[0],
                                            callback_data=Callbacks.MODERATE_REQUEST.format(r[0])))
    markup.add(*buttons)
    markup.add(InlineKeyboardButton(text=Buttons.BACK,
                                    callback_data=Callbacks.MODERATE_REQUEST.format('back')))

    return markup


def pay_in_markup(chat_id: int) -> ReplyKeyboardMarkup():
    keyboard = Keyboards.Menu.TX_IN_HISTORY if chat_id == megabite_id else None

    markup = _reply_markup(keyboard=keyboard,
                           chat_id=chat_id)

    return markup


def pay_out_markup(chat_id: int) -> ReplyKeyboardMarkup():
    keyboard = Keyboards.Menu.TX_OUT_HISTORY if chat_id == megabite_id else None
    markup = _reply_markup(keyboard=keyboard,
                           chat_id=chat_id)

    return markup


def handle_withdrawal_request(chat_id: int) -> ReplyKeyboardMarkup():
    keyboard = Keyboards.Menu.APPROVAL if chat_id == megabite_id else None

    markup = _reply_markup(keyboard=keyboard,
                           chat_id=chat_id)

    return markup


def confirm_out(chat_id: int) -> ReplyKeyboardMarkup():
    keyboard = Keyboards.Menu.CONFIRMATION_CHECK if chat_id == megabite_id else None

    markup = _reply_markup(keyboard=keyboard,
                           chat_id=chat_id)

    return markup


def delay_time(chat_id: int) -> ReplyKeyboardMarkup():
    markup = ReplyKeyboardMarkup(row_width=3)
    buttons = []
    [buttons.append(KeyboardButton(text=str(i))) for i in range(1, 10)]
    markup.add(*buttons)
    markup.add(*[Buttons.BACK, Buttons.MAIN_MENU])

    return markup


def deny_request(chat_id: int) -> ReplyKeyboardMarkup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(*[KeyboardButton(text=Buttons.BACK)])
    return markup


def history_inline(chat_id: int, username: str):
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=Buttons.TX_OUT_HISTORY,
                                    callback_data=Callbacks.PAY_OUT_HISTORY.format(username)),
               InlineKeyboardButton(text=Buttons.TX_IN_HISTORY,
                                    callback_data=Callbacks.PAY_IN_HISTORY.format(username))]
    markup.add(*buttons)

    return markup
