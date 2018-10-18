# coding: utf-8
# -*- coding: utf-8 -*-
# @Time    : 2018/10/11 0011 下午 6:56
# @Author  : antman-hu
# @Email   : 18819340421@163.com
# @File    : work1.py

'''
1.解析web请求地址为协议,主机名,端口,路径
2.爬取豆瓣的top250的数据，包括电影名,评分,评论人数,经典语录
'''

import socket, ssl


# 解析请求
def parase_url(url):
    protocol = 'http'
    port = 80
    path = '/'
    if url[:8] == 'https://':
        protocol, url = url.split('//')
        protocol = protocol[:5]
        port = 443
    elif url[:7] == 'http://':
        protocol, url = url.split('//')
        protocol = protocol[:4]

    if '/' in url:
        url, path = url.split('/', 1)
        path = '/' + path
        if len(path) == 0:
            path = '/'

    if ':' in url:
        url, port = url.split(':', 1)
        port = int(port)
    return (protocol, url, port, path)


def response_by_s(s):
    response = b''
    while True:
        r = s.recv(1024)
        if len(r) == 0:
            break
        response += r
    return response


def parase_response(response):
    hearders, body = response.split('\r\n\r\n', 1)
    hearder_list = hearders.split('\r\n')
    status = hearder_list.pop(0).split(' ')[1]
    headers_dict = {}
    for i in hearder_list:
        k, v = i.split(': ')
        headers_dict[k] = v
    return (status, headers_dict, body)


# 发起http请求

def get(url):
    protocol, url, port, path = parase_url(url)
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    http_request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, url)
    s.connect((url, port))

    s.send(http_request.encode('utf-8'))

    response = response_by_s(s)
    print(response)
    response = response.decode('utf-8')
    status, headers_dict, body = parase_response(response)
    if status == '301':
        print(headers_dict['Location'])
        return get(headers_dict['Location'])
    return (status, headers_dict, body)


status, headers_dict, body = get('http://movie.douban.com/top250')
print(status)
print(headers_dict)
print(body)