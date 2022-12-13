# import RPi.GPIO as GPIO
import time

import click
import pymysql


def turn_on_gpio(PIN):
    # print("GPIO.setmode(GPIO.BOARD)")
    # print("GPIO.setup(PIN, GPIO.OUT)")
    # print("GPIO.output(PIN, GPIO.HIGH)")
    time.sleep(0.03)

def turn_off_gpio(PIN):
    # print("GPIO.setmode(GPIO.BOARD)")
    # print("GPIO.setup(PIN, GPIO.OUT)")
    # print("GPIO.output(PIN, GPIO.LOW)")
    time.sleep(0.03)

# initPath = "./Init.yaml"

def mysql_db(no, t1, t2):
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
            t = time.time()
            # 准备SQL语句
            sql = f'update latency set first_line={t1}, last_line={t2} where req_no={no};';
            # 执行SQL语句
            cursor.execute(sql)
            # 执行完SQL语句后的返回结果都是保存在cursor中
            # 所以要从cursor中获取全部数据
            # datas = cursor.fetchall()
            conn.commit()
            # print("获取的数据：\n", datas)
    except Exception as e:
        print("数据库操作异常：\n", e)
    finally:
        # 不管成功还是失败，都要关闭数据库连接
        conn.close()


class LEDServer:
    def __init__(self):
        self.pLamp = 12

    def turn_on(self):
        turn_on_gpio(self.pLamp)

    def init(self):
        turn_off_gpio(self.pLamp)


@click.command()
@click.option('--no', default=0, type=int)
def run(no):
    t1 = time.time()
    led = LEDServer()
    led.init()
    led.turn_on()
    t2 = time.time()
    print(t2-t1)
    # mysql_db(no, t1, t2)


if __name__ == "__main__":
    run()
