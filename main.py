import threading
import time

from loguru import logger

from bot.db_calls import last_req_id
from bot.utils import start_bot_from_code, check_new_requests, exit_signal

if __name__ == '__main__':
    logger.info('Bot Started')

    check_new_requests()
    start_bot_from_code()

    try:
        while not exit_signal.is_set():  # enable children threads to exit the main thread, too
            time.sleep(0.1)  # let it breathe a little
    except KeyboardInterrupt:  # on keyboard interrupt...
        exit_signal.set()  # send signal to all listening threads
