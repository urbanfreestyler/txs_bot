from bot.buttons import Buttons


class Keyboards:
    class Menu:

        # NEW_REQUESTS = []
        TX_LIST = [[Buttons.MAIN_MENU]]
        TX_OUT_HISTORY = [[Buttons.MAIN_MENU]]
        TX_IN_HISTORY = [[Buttons.MAIN_MENU]]

        APPROVAL = [[Buttons.APPROVE, Buttons.APPROVE_DELAYED],
                    [Buttons.DENY],
                    [Buttons.BACK, Buttons.MAIN_MENU]]

        CONFIRMATION_CHECK = [[Buttons.YES],
                              [Buttons.NO]]

        CHECK_HISTORY = [
            [Buttons.TX_OUT_HISTORY, Buttons.TX_IN_HISTORY],
        ]