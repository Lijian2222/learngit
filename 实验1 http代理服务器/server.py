#===TCP服务端程序 server.py===
import re
import socket

#主机地址为0.0.0.0,表示绑定本机所有的网络接口ip地址
#等待客户端来连接
IP = '0.0.0.0'

#端口号
PORT = 50000

#定义一次从socket缓冲区最多读入512字节
BUFLEN = 1024

#实例化一个socket对象
#参数AF_INET表示该socket网络层使用IP协议
#参数SOCK_STREAM表示该socket传输层使用tcp协议
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#SOCKET绑定地址和端口
listenSocket.bind((IP,PORT))

#使用socket处于监听状态，等待客户端的连接请求
#参数5表示，最多接收5个等待连接的客户端
listenSocket.listen(5)
print(f"服务器端启动成功，在{PORT}端口等待客户端连接...")

#这里产生了一个新的dataSocket,用来传输数据用的
dataSocket,addr=listenSocket.accept()
print("接收一个客户端连接：",addr)

while True:
    #尝试读取对方发送的消息
    #BUFLEN指定从接受缓冲里最多读取多少字节
    recved = dataSocket.recv(BUFLEN)

    #如果返回空bytes,表示对方关闭了连接
    #退出循环，结束消息收发
    # if not recved:
    #     break

    #读取到的数据是bytes类型，需要解码为字符串
    info = recved.decode()

    print(f'收到对方信息：{info}')
    print("========================================================================")
    dataSocket.sendall(b"HTTP/1.0 200 Connection Established\r\n\r\n")
    # global serverSocket
    # try:
    #     # url=re.search('www\.([a-z]+\.)+com',info).group()
    #     serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     serverSocket.connect(("www.baidu.com",80))
    #     serverSocket.send("GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n".encode())
    #     recv1=serverSocket.recv(1024*1000)
    #     print("百度返回信息",recv1)
    #     dataSocket.send(recv1)
    # except AttributeError:
    #     print("info正则表达式匹配失败")
    #     serverSocket.send(recved) #直接转发
    #     recv2=serverSocket.recv(1024*1000)
    #     dataSocket.send(recv2) #直接返回
    # #发送的数据类型必须是bytes,所以要编码
    # # dataSocket.send(f"服务器端收到了信息{info}".encode())

#服务器端也调用close()关闭socket
dataSocket.close()
# listenSocket.close()
