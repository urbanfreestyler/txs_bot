class Messages:

    START_MESSAGE = 'Вы в главном меню'

    PAY_IN_HISTORY = "Пополнение №{}\n\nПочта: {}\nЛогин: {}\nСумма: {}$\nВремя: {}\nСистема оплаты: {}"

    PAY_OUT_HISTORY = "Вывод №{}\n\nПочта: {}\nЛогин: {}\nСумма: {}$\nВремя: {}\nСистема оплаты: {}"

    WITHDRAWAL_REQUESTS = "Запрос №<b>{}</b>\n\n" \
                          "Почта: <b>{}</b>\nЛогин: <b>{}</b>\n" \
                          "Сумма: <b>{}</b>$\n" \
                          "Время: <b>{}</b>\n" \
                          "Кошелёк вывода: <i>{}</i>\n" \
                          "Количество процессоров: <b>{}</b>, (cумма: <b>{}</b>$)\n" \
                          "Количество денег в обмене: <b>{}</b>\n" \
                          "Количество денег в ордерах: <b>{}</b>\n" \
                          "Количество рефералов: <b>{}</b>\n" \
                          "Сумма пополнений рефералов: <b>{}$</b>\n" \
                          "Реферальный баланс: <b>{}</b>\n "

    NO_NEW_REQUESTS = 'Новых запросов пока нет'

    NEW_REQUESTS = "Список новых запросов на вывод\nНажмите на айди, чтобы открыть запрос"

    CONFIRMATION_QUESTION = "Вы действительно хотите одобрить вывод средств?"

    DELAY_TIME_INPUT = 'Выберите или введите кол-во часов перед выплатой'

    NEXT_ACTION = 'Выберите действие'

    NO_PAY_OUT_BEFORE = "Этот пользователь ещё не выводил средств."

    APPROVE_SUCCESS = 'Успешно подтвержден запрос на вывод №<b>{}</b>'

    APPROVE_ERROR = 'Не удалось подтвердить вывод платежа №<b>{}</b>'

    TO_REQUESTS = 'Найдено <b>{}</b> запросов'

    DENIAL_REASON = 'Напишите причину отказа выплаты'

    DENIED_SUCCESSFULLY = "✅ Вывод успешно отклонён"