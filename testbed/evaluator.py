import time

import pika
import redis
import requests
from taosrest import connect, TaosRestConnection, TaosRestCursor
import pymysql
from base_thread import BaseThread

# --------------------------------------------------------------------------------------------------------------#
# Init Redis
r = redis.Redis(host='10.214.131.191', port=6379, db=0, decode_responses=True)
# md5encoder = hashlib.md5()

# Init RabbitMQ
user_info = pika.PlainCredentials('root', 'root')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.214.131.191', 5672, 'myvhost', user_info))
channel = connection.channel()

# 如果指定的queue不存在，则会创建一个queue，如果已经存在 则不会做其他动作，生产者和消费者都做这一步的好处是这样生产者和消费者就没有必要的先后启动顺序了
channel.queue_declare(queue='trigger')

conn: TaosRestConnection = connect(url="http://10.214.131.191:6041", user="root", password="taosdata", timeout=30)
cursor: TaosRestCursor = conn.cursor()

# --------------------------------------------------------------------------------------------------------------#
def check_valid(trigger, rule):
    print(rule["Triggers"])
    triggers = rule["Triggers"].split(',')
    triggers.remove(trigger)  # 去除掉当前valid的trigger
    for t in triggers:
        cursor.execute("SELECT * FROM valid.{} LIMIT 1".format(t))  # 从valid数据库中对应的trigger表中获取一个数据
        if cursor.rowcount == 0:  # 没有查到
            return False
    # TODO: add item to TDEngine
    # TODO: check condition
    return True


def actuate_func(func_id, req_no):
    function = r.hgetall(func_id)
    func_name = function["name"]
    print(f'call: {func_name}')
    t = time.time()
    sql = f'update latency set call_func = {t} where req_no={req_no};'
    mysql_db(sql)
    args = {"req_no": f'{req_no}'}
    res = requests.get('http://10.214.131.192:9211/func/{}'.format(func_name), params=args)
    return res.text


# channel: 包含channel的一切属性和方法
# method: 包含 consumer_tag, delivery_tag, exchange, redelivered, routing_key
# properties: basic_publish 通过 properties 传入的参数
# body: basic_publish发送的消息
def callback(ch, method, properties, body):
    request = body.strip().decode('utf-8').split(',')
    print(f'request:{request}')
    key = request[0]
    req_no = request[2]
    t = time.time()
    sql = f'update latency set rabbit_consume = {t} where req_no = {req_no};'
    mysql_db(sql)
    # key = body.strip().decode('utf-8').replace(',', '')  # temperature
    # TODO: multi-trigger like: temperature,camera
    num_of_related_rules = r.llen(key)  # 某个trigger对应的rules
    check_threads = []
    rules = []
    exec_threads = []
    for i in range(num_of_related_rules):
        rid = r.lindex(key, i)  # rules集合中的某条rule
        rule = r.hgetall(str(rid))
        t = BaseThread(target=check_valid, args=(key, rule,))
        check_threads.append(t)
        rules.append(rule)
        t.start()
    for i in range(num_of_related_rules):
        check_threads[i].join()
        if check_threads[i].get_result():
            actions = rules[i]["Actions"].split(',')
            for action in actions:
                action = action.replace('\'', '')
                t = BaseThread(target=actuate_func, args=(action, req_no,))
                exec_threads.append(t)
                t.start()
    for t in exec_threads:
        t.join()
        # print(t.get_result())
        # TODO: use rabbitMQ to return the actuation id back to the user

def mysql_db(str):
    # 连接数据库肯定需要一些参数
    conn = pymysql.connect(
        host="10.214.131.191",
        port=3306,
        database="docker_log",
        charset="utf8",
        user="log",
        passwd="1"
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(str)
            # 执行完SQL语句后的返回结果都是保存在cursor中
            # 所以要从cursor中获取全部数据
            # datas = cursor.fetchall()
            conn.commit()
            print(f'successfully run: {str}')
    except Exception as e:
        print("数据库操作异常：\n", e)
    finally:
        # 不管成功还是失败，都要关闭数据库连接
        conn.close()
# --------------------------------------------------------------------------------------------------------------#
channel.basic_consume(queue='trigger', auto_ack=True, on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')

# 一直处于等待接收消息的状态，如果没收到消息就一直处于阻塞状态，收到消息就调用上面的回调函数
channel.start_consuming()
