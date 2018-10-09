# coding: utf-8
# -*- coding: utf-8 -*-
# @Time    : 2018/10/9 0009 下午 6:33
# @Author  : antman-hu
# @Email   : 18819340421@163.com
# @File    : web-client.py


import socket

'''
web客户端流程
1.创建socket通道
2.构建请求信息
3.二进制模式发送请求内容
4.接收服务器响应信息
5.将服务器响应的二进制内容解码成str类型内容
'''

s = socket.socket()

host = '127.0.0.1'
port = 2000

s.connect((host,port))

ip,port = s.getsockname()
print('ip和port是{0}：{1}'.format(ip,port))

http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)

request = http_request.encode('utf-8')
print('请求{}'.format(request))

s.send(request)

#括号内表示接收的服务器响应回来的信息的长度，超过长度的不会接收
response = s.recv(10230)
print('响应信息是{}'.format(response.decode('utf-8')))
