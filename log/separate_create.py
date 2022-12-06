import time

import docker
from flask import Flask
from flask import request

from utils.MySQL_writer import MySQLWriter
from utils.file_writer import FileWriter

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
    t1 = time.time()
    no = request.args.get('no')
    t2 = time.time()
    client = docker.from_env()
    t3 = time.time()
    client.containers.run('sleep', command=f'python3 sleep.py --no {no}', name=f'sleep_{no}')
    t4 = time.time()
    mysql = MySQLWriter("10.214.131.191", "docker_log", "log", "1")
    mysql.sql_exe(f'update log3 set a={t1} where no = 1 ')
    t5 = time.time()
    t6 = time.time()
    file = FileWriter("./separate.txt")
    file.write(f'{t1},{t2},{t3},{t4},{t5},{t6}')
    # return
    return no


def run_exe():
    time.sleep(0.01)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
