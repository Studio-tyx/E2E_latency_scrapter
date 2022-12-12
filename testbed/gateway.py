import time
import docker
from flask import Flask, request
from get_inspect import get_time
from MySQL_writer import MySQLWriter

app = Flask(__name__)


@app.route('/')
def liveness_probe():
    return "server is alive."


@app.route('/func/<string:func_id>')
def call_func(func_id):
    mysql = MySQLWriter("10.214.131.191", "docker_log", "log", "1")
    req_no = request.args.get('req_no')
    t = time.time()
    mysql.sql_exe(f'update latency set gateway_func={t}, container_ID=\'{func_id}_{req_no}\' where req_no = {req_no};')
    client = docker.from_env()
    print(func_id)
    print(client.containers.run('sleep:1.0', command=f'python3 sleep.py --no {req_no}', name=f'sleep_{req_no}'))
    get_time(container_name=f'{func_id}_{req_no}')
    print(client.containers)
    container = client.containers.get(f'sleep_{req_no}')
    print(container.remove(force=True))
    return "function {} is called".format(func_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9211)
