import pika

# 连接rabbitmq
user_info = pika.PlainCredentials('root', 'root')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.214.131.191', 5672, 'myvhost', user_info))
channel = connection.channel()

# 声明队列
channel.queue_declare(queue='hello')

# 插入数据
# exchange='' 指定为简单模式
# routing_key='hello' 指定队列
# body='Hello World!' 指定内容
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

connection.close()