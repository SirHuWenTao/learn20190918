# coding: utf-8
# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 0023 下午 7:15
# @Author  : antman-hu
# @Email   : 18819340421@163.com
# @File    : work2.py


import socket, ssl
from bs4 import BeautifulSoup


# 定义log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


# 作业 2.1
#
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    path_u = ''
    for k in query.keys():
        path_u = path_u + ''.join([k, '=', str(query[k]), '&'])
    path_u = ''.join([path, '?', path_u])
    return path_u


def test_path_with_query():
    # 注意 height 是一个数字
    path = '/'
    query = {
        'name': 'gua',
        'height': 169,
    }
    expected = [
        '/?name=gua&height=169',
        '/?height=169&name=gua',
    ]
    # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
    assert path_with_query(path, query) in expected


# 作业 2.2
#
# 为作业1 的 get 函数增加一个参数 query
# query 是字典
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


# 处理服务器响应的信息

def parase_response(response):
    headers, body = response.split('\r\n\r\n', 1)
    header_list = headers.split('\r\n')
    status = header_list.pop(0).split(' ')[1]
    headers_dict = {}
    for i in header_list:
        k, v = i.split(': ')
        headers_dict[k] = v
    return (status, headers_dict, body)


# 发起http请求

def get(url, query):
    protocol, url, port, path = parase_url(url)
    path = path_with_query(path, query)
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    http_request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, url)
    s.connect((url, port))

    s.send(http_request.encode('utf-8'))

    response = response_by_s(s)
    response = response.decode('utf-8')
    status, headers_dict, body = parase_response(response)
    if status == '301':
        return get(headers_dict['Location'])
    return (status, headers_dict, body)


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
    response = response.decode('utf-8')
    status, headers_dict, body = parase_response(response)
    if status == '301':
        return get(headers_dict['Location'])
    return (status, headers_dict, body)


# 作业 2.3
#
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
    	'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    headers_str = ''
    for k, v in headers.items():
        headers_str = ''.join([headers_str, k, ': ', str(v), '\\r\\n'])
    return headers_str
    # 作业 2.4


#
# 为作业 2.3 写测试
def test_header_from_dict():
    headers = {
        'Content-Type': 'text/html',
        'Content-Length': 127,
    }
    expected = [
        "Content-Type: text/html\\r\\nContent-Length: 127\\r\\n",
        "Content-Length: 127\\r\\nContent-Type: text/html\\r\\n"
    ]
    assert header_from_dict(headers) in expected


# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client_ssl.py 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""


def parase_html(url):
    status, headers_dict, body = get(url)

    soup = BeautifulSoup(body, "lxml")

    film_info_lists = soup.find_all('div', attrs={'class': ['info']})
    for film_info in film_info_lists:
        file_name = film_info.find('span', attrs={'class': ['title']}).text
        score = film_info.find('span', attrs={'class': ['rating_num']}).text
        evaluate_people = film_info.find('span', attrs={'property': ['v:best']}).next_element.next_element.text
        quote = film_info.find('span', attrs={'class': ['inq']}).text
        print(file_name)
        print(score)
        print(evaluate_people)
        print(quote)
        print('-' * 20)




# 作业 2.6
#

"""
循环爬出豆瓣 top250 https://movie.douban.com/top250的所有网页
s观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

"""


def get_douban_datas():
    for num in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(num * 25)
        parase_html(url)

if __name__ == '__main__':
    parase_html('https://movie.douban.com/top250?start=0&filter=')
    get_douban_datas()
