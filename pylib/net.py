#! /usr/bin/env python
import time
import requests


def req(url):
    i = 0
    flag = 0
    while i < 10:

        i = i + 1
        # 十次连接失败后要检测网络连接是否正常，不正常则阻塞在循环里
        if i == 10:
            netStatus = testNet()
            if netStatus == 0:
                time.sleep(5)
                i = 9

        try:
            resp = requests.get(url, verify=False, timeout=20)

            if resp.status_code == 200:
                flag = 1
                break
        except requests.exceptions.RequestException:
            continue

    if flag == 1:
        return resp
    else:
        return False


def testNet():
    try:
        response = requests.get('https://www.baidu.com', verify=False, timeout=20)
        if response.status_code ==200:
            return 1
        if response.status_code ==404:
            return 0
    except requests.exceptions.RequestException:
        return 0
    return 1