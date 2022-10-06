from bot.db_calls import get_new_requests


class Buttons:
    # Main menu buttons
    TX_IN_HISTORY = '💸 История пополнений'
    TX_OUT_HISTORY = '💸 История выводов'
    TX_NEW = "🆕 Новые запросы [{}]"

    # Navigation
    BACK = '◀️ Назад'
    MAIN_MENU = '🏘 Главное меню'

    # Tx approval
    DENY = '❌ Отказать'
    APPROVE_DELAYED = '✅🕔 Одобрить с задержкой'
    APPROVE = '✅ Одобрить'
    NEXT = 'След. ➡️'
    PREV = '⬅️ Пред.'
    LEFT = '⬅️'
    RIGHT = '➡️'

    YES = '✅ Да'
    NO = '❌ Нет'


class Callbacks:
    NEW_REQUEST = 'request_{}'
    MODERATE_REQUEST = 'moderate_{}'

    PAY_IN_HISTORY = 'pay_in_{}'
    PAY_OUT_HISTORY = 'pay_out_{}'

    LEFT = 'left'
    RIGHT = 'right'
