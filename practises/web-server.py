# coding: utf-8
# -*- coding: utf-8 -*-
# @Time    : 2018/10/9 0009 下午 6:49
# @Author  : antman-hu
# @Email   : 18819340421@163.com
# @File    : web-server.py


import socket

'''
1.创建socket通道
2.绑定服务器的地址及端口
3.无限循环接收客户端请求
4.设置监听
5.接收客户端请求
6.返给客户端响应信息
7.关闭请求，等待下个客户端请求
'''

host = ''
port = 2000

s = socket.socket()
s.bind((host,port))

while True:
    s.listen(5)
    connection,addr = s.accept()
    request = connection.recv(1024)
    print('ip and request {0} - {1}'.format(addr,request.decode('utf-8')))

    response = b'<h1>hello world</h1>'
    connection.sendall(response)
    connection.close()