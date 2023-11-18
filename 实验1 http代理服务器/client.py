#===TCP客户端程序===
import socket

IP='127.0.0.1'
SERVER_PORT=50000
BUFLEN=1024

#实例化一个socket对象，指明协议
#参数AF_INET表示该socket网络层使用IP协议
#参数SOCK_STREAM表示该socket传输层使用tcp协议
dataSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#连接服务器端socket
dataSocket.connect((IP,SERVER_PORT))

while True:
    #从终端读入用户输入的字符串
    toSend = input('>>')
    if toSend == "exit":
        break
    #发送消息，也要编码为bytes
    dataSocket.send(toSend.encode())

    #等待接受服务端的消息
    recved = dataSocket.recv(BUFLEN)
    #如果返回了空bytes,表示对方关闭了连接
    if not recved:
        break
    #打印读取的信息
    print(recved.decode())

dataSocket.close()