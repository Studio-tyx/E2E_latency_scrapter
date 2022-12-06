# import pika
#
# #你的RabbitMQ的地址
# host = "10.214.131.191"
# #RabbitMQ端口号
# post = 5672
# #创建的账号，当然了也可以使用默认的guest账号，密码也是guest
# username = "root"
# #账号的密码
# password = "root"
#
# # 创建一个有凭证的新实例
# credentials = pika.PlainCredentials(username, password)
# # 使用凭证连接RabbitMQ服务器
# connection = pika.BlockingConnection(pika.ConnectionParameters(host,post,credentials=credentials))
# #声明一个管道
# channel = connection.channel()
#
# #指定队列的名字
# queueName="hello"
#
# #说明使用的队列，如果没有会自动创建
# channel.queue_declare(queueName)
#
# #发送的msg消息
# msg = "Hello TrueDei"
#
# #n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
# channel.basic_publish(exchange='', routing_key=queueName, body=msg)
# print(" [x] Sent 'Hello TrueDei'")
# connection.close()

# coding=utf-8
### 生产者

import pika
import time

user_info = pika.PlainCredentials('root', 'root')  # 用户名和密码
connection = pika.BlockingConnection(pika.ConnectionParameters('10.214.131.191', 5672, 'myvhost', user_info))  # 连接服务器上的RabbitMQ服务

# 创建一个channel
channel = connection.channel()

# 如果指定的queue不存在，则会创建一个queue，如果已经存在 则不会做其他动作，官方推荐，每次使用时都可以加上这句
channel.queue_declare(queue='hello')

for i in range(0, 100):
    channel.basic_publish(exchange='',  # 当前是一个简单模式，所以这里设置为空字符串就可以了
                          routing_key='hello',  # 指定消息要发送到哪个queue
                          body='Hello World!'  # 指定要发送的消息
                          )
    time.sleep(1)

# 关闭连接
# connection.close()