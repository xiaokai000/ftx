import requests


def get_proxies():

    base_url = 'http://webapi.http.zhimacangku.com/getip?num=%d&type=2&pro=&city=0&yys=0&port=11&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=2&regions='

    number = 5

    proxies = []

    for proxy in requests.get(base_url%number).json()['data']:
        ip = proxy['ip']
        port = proxy['port']

        s = 'https://' + ip + ":" + str(port)
        proxies.append(s)


    with open('proxy.py', 'w') as f:

        f.write('PROXY = [')
        for i in proxies:
            f.write('"' + i + '"' + ',')
        f.write(']')

    return proxies

get_proxies()