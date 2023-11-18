# encoding:utf-8
import socket
import _thread


class Header:
    """
    用于读取和解析头信息
    """

    def __init__(self, conn):
        self._method = None
        header = b''
        try:
            while 1:
                data = conn.recv(4096)   # conn接收数据
                header = b"%s%s" % (header, data) #每次接收的data做一个字符串相加
                if header.endswith(b'\r\n\r\n') or (not data): #GET请求末尾一般都是\r\n\r\n,普通data就判断空不空
                    break
        except:
            pass
        self._header = header
        self.header_list = header.split(b'\r\n') #把收到的请求按回车分开，放到数组里面
        self._host = None
        self._port = None

    def get_method(self):
        """
        获取请求方式
        :return:
        """
        if self._method is None:
            self._method = self._header[:self._header.index(b' ')]  #self._method也是一个字符串，例如GET
        return self._method

    def get_host_info(self):
        """
        获取目标主机的ip和端口
        :return:
        """
        if self._host is None:
            method = self.get_method() #拿到self._method字符串，要么是GET要么是CONNECT
            line = self.header_list[0].decode('utf8') #拿到GET或者CONNECT第一行数据，如GET http://www.baidu.com/ HTTP/1.1
            if method == b"CONNECT":
                host = line.split(' ')[1] #拿到目的url,如
                if ':' in host:
                    host, port = host.split(':')
                else:  #如果没写明port,默认443
                    port = 443
            else:  #如果是GET请求
                for i in self.header_list:
                    if i.startswith(b"Host:"): #找到Host开头的表项，如果没找到或者Host表项没有地址，就不会break，就会执行下面的else
                        host = i.split(b" ")
                        if len(host) < 2:  #处理某些特殊情况，正常不会执行该步骤，正常刚好等于2，如Host: www.baidu.com:443
                            continue
                        host = host[1].decode('utf8')
                        break
                else:  #没有找到host (for循环正常结束后要执行的代码，break后不用执行)
                    host = line.split('/')[2]  #处理某些特殊情况
                if ':' in host:
                    host, port = host.split(':')
                else: #默认80端口
                    port = 80
            self._host = host
            self._port = int(port)
        return self._host, self._port

    @property
    def data(self):
        """
        返回头部数据
        :return:
        """
        return self._header

    def is_ssl(self):
        """
        判断是否为 https协议
        :return:
        """
        if self.get_method() == b'CONNECT': #http默认80端口，https默认443端口，CONNECT都是443端口，GET都是80端口
            return True
        return False

    def __repr__(self):
        return str(self._header.decode("utf8"))


def communicate(sock1, sock2):
    """
    socket之间的数据交换
    :param sock1:
    :param sock2:
    :return:
    """
    try:
        while 1:
            data = sock1.recv(1024)  # client 收数据
            if not data:
                return
            sock2.sendall(data)  #代理发给服务器
    except:
        pass


def handle(client):
    """
    处理连接进来的客户端
    :param client:
    :return:
    """
    timeout = 60  #60秒
    client.settimeout(timeout)  #设置超时断开连接，防止大量死连接占用端口
    header = Header(client)  #封装成类并初始化，对接收的请求进行处理
    if not header.data: #如果接收到的数据为空，就断开连接
        client.close()
        return       #get_host_info返回ip和port,  get_method返回GET或者CONNECT
    print(*header.get_host_info(), header.get_method())  #加*号可以循环打印
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #创建一个socket(server)
    print("创建server socket")
    try:
        server.connect(header.get_host_info()) #返回元组(ip,port),  代理服务器连接服务器
        server.settimeout(timeout)  #设置超时时间
        if header.is_ssl(): #如果是https协议(如果是CONNECT请求)，回复一个http 200
            data = b"HTTP/1.0 200 Connection Established\r\n\r\n" #代理服务器给客户端返回http 200 响应,此时建立了原始数据的任意双向通信，直到连接关闭为止
            client.sendall(data)   # 代理服务器返回客户端
            _thread.start_new_thread(communicate, (client, server)) #创建一个新线程开始原始数据的任意双向通道，客户端发给服务器
        else: #如果是http协议(如果是GET请求)，直接把header发过去
            server.sendall(header.data)  #直接向服务器发送请求
        communicate(server, client)   # 服务器发给客户端
    except:  #没连上的直接关闭socket
        server.close()
        client.close()


def serve(ip, port):
    """
    代理服务
    :param ip:
    :param port:
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建一个socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #套接字端口重用，允许重用本地地址和端口(端口释放后就可以立即被再次使用)
    s.bind((ip, port))  #socket绑定端口
    s.listen(10)  #开始监听
    print('proxy start...')
    while True:
        conn, addr = s.accept()  #接收连接，创建一个新的socket(conn)负责数据通信，拿到对面的ip地址
        print("创建子线程")
        _thread.start_new_thread(handle, (conn,))  #创建一个子线程处理收到的请求


if __name__ == '__main__':
    IP = "127.0.0.1"
    PORT = 50000
    serve(IP, PORT)