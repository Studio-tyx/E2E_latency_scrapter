# import taos
#
# conn: taos.TaosConnection = taos.connect(host="10.214.131.191",
#                                          user="root",
#                                          password="root",
#                                          database="test",
#                                          port=6030,
#                                          timezone="Asia/Shanghai")  # default your host's timezone
#
# server_version = conn.server_info
# print("server_version", server_version)
# client_version = conn.client_info
# print("client_version", client_version)  # 3.0.0.0
#
# conn.close()
from taosrest import connect, TaosRestConnection, TaosRestCursor

conn: TaosRestConnection = connect(url="http://10.214.131.191:6041", user="root", password="taosdata", timeout=30)
cursor: TaosRestCursor = conn.cursor()
cursor.execute("show databases;")
print("databases:", cursor.rowcount)