import redis
import hashlib
import sys
from taosrest import connect, TaosRestConnection, TaosRestCursor

def main(args=None):
    conn: TaosRestConnection = connect(url="http://10.214.131.191:6041", user="root", password="taosdata", timeout=30)
    cursor: TaosRestCursor = conn.cursor()
    cursor.execute("SELECT * FROM valid.{} LIMIT 1".format("temperature"))  # 从valid数据库中对应的trigger表中获取一个数据
    print(cursor.rowcount)


if __name__ == '__main__':
    sys.exit(main())