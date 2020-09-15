# -*- coding:utf-8 -*-

"""

    Created by liuyi.shen
    
    Created on 2020/7/23
          
"""
import ConfigParser
import codecs
import os

import redis

class redisclient(object):

    def __init__(self,host,port,password):

        self.rc = redis.Redis(host=host, port=port, password=password)

    def lpush(self,key,value):

        self.rc.lpush(key,value)

    def delete(self,names):

        self.rc.delete(names)


if __name__ == '__main__':

    cf=ConfigParser.ConfigParser()

    cf.read("config.cfg")

    host=cf.get("redis","host")

    port=cf.get("redis", "port")

    rc=redisclient(host,port,'')

    urlKey = cf.get("redis", "urlKey")

    deleteKey = cf.get("redis", "deleteKey")

    if "," in deleteKey:

        keys = deleteKey.split(",")

        for key in keys:

            if key != "":

                rc.delete(key)

                print("redis key:" + str(key) + " deleted")

    elif deleteKey != "":

        rc.delete(deleteKey)

        print("redis key:" + str(deleteKey) + " deleted")

    urlFile=cf.get("redis", "urlFile").decode("utf-8")

    f1=codecs.open(urlFile,'r')

    for line in f1:

        rc.lpush(urlKey,line.strip("\r\n"))

    f1.close()

    print("url file:" + str(urlFile) + " imported")

    os.system('pause')