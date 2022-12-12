import pika

# 连接rabbitmq
user_info = pika.PlainCredentials('root', 'root')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.214.131.191', 5672, 'myvhost', user_info))
channel = connection.channel()

# 声明队列
channel.queue_declare(queue='hello')

# 定义回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

# 确定监听队列
channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)

# 启动监听
channel.start_consuming()