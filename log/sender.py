import time

import requests

from utils.MySQL_writer import MySQLWriter

__sleep_url__ = "http://10.214.131.191:5000/sleep1000"
__light_url__ = "http://10.214.131.191:5000/light"


def send_no(url, no):
    t = time.time()
    args = {"no": f'{no}'}
    # file=FileWriter("./log/log.txt")
    # file.write(f'{no},{t}')
    mysql = MySQLWriter("10.214.131.191", "docker_log", "log", "1")
    mysql.sql_exe(f'insert into log2 (no,sendtime) values ({no},{t});')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    response = requests.get(url, params=args, headers=headers)


if __name__ == '__main__':
    # for no in range(5):
    #     id =no
    #     send_no(__node1_url__,id)
    no = 100
    send_no(f'{__light_url__}', no)
    # no = 5
    # send_no(f'{__node1_url__}{no}', no)
    # no = 6
    # send_no(f'{__node1_url__}{no}', no)
    # no = 7
    # send_no(f'{__node1_url__}{no}', no)
