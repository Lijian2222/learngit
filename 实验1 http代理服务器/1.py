import socket


def proxy_server():
    # 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 监听端口
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)

    print('代理服务器已启动，监听端口 8080...')

    while True:
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print('接收到来自 %s 的连接' % str(client_address))

        # 接收客户端请求
        request = client_socket.recv(1024)
        print('接收到请求：\n%s' % request.decode())

        # 解析请求
        method, url, protocol = parse_request(request)
        print('解析请求：\n方法：%s\nURL：%s\n协议：%s' % (method, url, protocol))

        # 发送请求给目标服务器
        response = send_request(method, url, protocol)
        print('接收到响应：\n%s' % response.decode())

        # 将响应发送给客户端
        client_socket.sendall(response)

        # 关闭连接
        client_socket.close()


def parse_request(request):
    # 解析请求行
    lines = request.decode().split('\r\n')
    method, url, protocol = lines[0].split(' ')

    return method, url, protocol


def send_request(method, url, protocol):
    # 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 解析 URL
    _, _, host, path = url.split('/', 3)

    # 连接目标服务器
    server_socket.connect((host, 80))

    # 构造请求
    request = f'{method} /{path} {protocol}\r\nHost: {host}\r\n\r\n'

    # 发送请求
    server_socket.sendall(request.encode())

    # 接收响应
    response = b''
    while True:
        data = server_socket.recv(1024)
        if not data:
            break
        response += data

    # 关闭连接
    server_socket.close()

    return response


# 启动代理服务器
proxy_server()