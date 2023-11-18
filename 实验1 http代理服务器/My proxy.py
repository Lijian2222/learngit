import _thread
import socket

class request:
    def __init__(self,client_socket:socket):
        self.header=b""
        while True:
            data=client_socket.recv(1024)
            self.header=b"%s%s"%(self.header,data)
            if data.endswith(b"\r\n\r\n") or not data:
                break
        print("header:",self.header)
        self.header_list=self.header.split(b"\r\n")
        self.host=""
        self.port=443 #默认80端口
        self.method=""
        line = self.header_list[1].decode()
        host = line.split(" ")[1]
        if ":" in host:
            host, port = host.split(":")
            self.port = int(port)
        self.host = host
        line = self.header_list[0].decode()
        self.method=line.split(" ")[0]



def communicate(sock1,sock2):
    while True:
        data=sock1.recv(1024)
        if not data:  #数据为空，方法结束
            return
        sock2.sendall(data)

def work(client):
    client.settimeout(60)
    re = request(client)  # 封装成类，面向对象处理
    if not re.header: #如果请求为空
        client.close() #关闭连接
        return #方法结束
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 请求不为空，创建一个socket连接服务器
    print("创建socket")
    try:
        server.connect((re.host,re.port))  #代理服务器连接服务器
        print(re.host, re.port, "已连接")

        if re.method=="CONNECT":  #CONNECT请求没有请求体，因为它的目的是建立隧道连接，所以服务器不需要返回资源
            print("CONNECT")
            client.sendall(b"HTTP/1.0 200 Connection Established\r\n\r\n") #回复客户端，建立数据原始通道
            _thread.start_new_thread(communicate,(client,server))  #创建一个线程负责客户对服务器！！！
        else:  #GET才会请求资源，需要服务器对客户端返回资源
            print("GET")
            server.sendall(re.header)
        communicate(server,client) #本身线程负责服务器对客户
    except:  #没连上的或者超时的直接关闭socket
        client.close()
        server.close()

def handle(ip,port):
    proxy=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建一个socket(ipv4,tcp)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 套接字端口重用，允许重用本地地址和端口(端口释放后就可以立即被再次使用)
    proxy.bind((ip,port))  #绑定端口
    proxy.listen(10) #开始监听
    print(f"代理服务器启动成功，在{port}端口等待连接")

    while True:  #访问一个网站需要多个
        client, addr = proxy.accept()
        print(f"收到客户端{addr}的请求")
        _thread.start_new_thread(work,(client,)) #创建子线程去处理




if __name__ == "__main__":
    IP="127.0.0.1"
    PORT=50000
    handle(IP,PORT)








