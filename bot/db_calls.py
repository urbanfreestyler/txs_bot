# cur helps to make db calls
import time

from loguru import logger

from global_vars import cur


def get_new_requests():
    cur.execute('SELECT * FROM dle_payout WHERE status = 0 ORDER BY id DESC')

    new_requests = cur.fetchall()

    return new_requests


def get_request(r_id: str):
    cur.execute('SELECT * FROM dle_payout WHERE id = ' + r_id)
    r = cur.fetchone()

    return r


def get_pay_in_history(username: str):
    cur.execute('SELECT * FROM dle_payin WHERE username = %s', (username,))

    new_requests = cur.fetchall()

    return new_requests


def get_pay_out_history(username: str):
    cur.execute('SELECT * FROM dle_payout WHERE status = 1 AND username = %s', (username,))

    new_requests = cur.fetchall()

    return new_requests


def get_user_cpu_info(username):
    proc_num = 0
    proc_total_price = 0
    ref_earned = 0

    cur.execute("SELECT qty, price FROM dle_user_cpu WHERE username = %s", (username,))
    cpu_info = cur.fetchall()
    info = cpu_info
    for i in info:
        proc_num += int(i[0])
        proc_total_price += int(i[0]) * int(i[1])
    cur.execute("SELECT earned FROM dle_referals WHERE name = %s", (username,))
    ref_sum = cur.fetchall()
    ref_num = len(ref_sum)
    for s in ref_sum:
        ref_earned += int(s[0])
    # print(earned)

    return proc_num, proc_total_price, ref_num, ref_earned


def approve_withdrawal(r_id: str):
    try:
        cur.execute("UPDATE dle_payout SET status=1 WHERE id = %s", (r_id,))
        cur.fetchall()
        return True
    except Exception as e:
        logger.error(e)
        return False


def approve_with_delay(username: str, time: str):
    try:
        cur.execute("UPDATE dle_payout SET dateout = %s WHERE username = %s", (time, username,))
        cur.fetchall()
        return True
    except Exception as e:
        logger.error(e)
        return False


def deny_withdrawal_request(r_id: str, description: str):
    try:
        cur.execute("UPDATE dle_payout SET status=3 WHERE id=%s", (r_id,))
    except Exception as e:
        logger.error(e)


def last_req_id():
    cur.execute('SELECT id from dle_payout WHERE status = 0 ORDER BY id DESC LIMIT 1')
    last = cur.fetchall()[0]
    return last[0]
