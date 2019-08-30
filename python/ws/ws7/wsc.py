import time
from websocket import create_connection
# ws = create_connection("ws://192.168.1.39")

url = "ws://192.168.1.39/websocket"
while True:  # 一直链接，直到连接上就退出循环
    time.sleep(2)
    try:
        ws = create_connection(url)
        print(ws)
        break
    except Exception as e:
        print('连接异常：', e)
        continue