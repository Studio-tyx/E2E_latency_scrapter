import sys
import time

import docker
from flask import Flask
from flask import request

from utils.MySQL_writer import MySQLWriter

app = Flask(__name__)


# 根路由，用来读取HTTP请求头数据
@app.route('/')
def index():
    # 读取HTTP请求头的User-Agent字段值
    user_agent = request.headers.get('User-Agent')
    return '<h1>Your browser is %s</h1>' % user_agent


# 用于读取GET请求数据的路由
@app.route('/sleep1000')
def time_record():
    # 读取GET请求中的arg字段值
    no = request.args.get('no')
    # run_exe()
    t = time.time()
    client = docker.from_env()
    print(client.containers.run('sleep', command=f'python3 sleep.py --no {no}', name=f'sleep_{no}')) # 容器第一行不测的话可以不用写no
    mysql = MySQLWriter("10.214.131.191", "docker_log", "log", "1")
    mysql.sql_exe(f'update log2 set recetime={t} where no={no};')
    return no


__path__ = "./rece_log.txt"


def log_write(string):
    stdout_backup = sys.stdout
    log_file = open(__path__, "a")
    sys.stdout = log_file
    print("writen log successfully: " + string)
    log_file.close()
    sys.stdout = stdout_backup


# log_write()
def run_exe():
    time.sleep(0.01)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
