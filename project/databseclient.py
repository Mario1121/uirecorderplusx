# -*- coding:utf-8 -*-

"""

    Created by liuyi.shen
    
    Created on 2020/7/13
          
"""
import traceback

import pymysql

import sys

import ConfigParser

import redis

class databseclient(object):

    def __init__(self):
        pass

    def execSqlCmd(self):
        pass


class mysqlclient(databseclient):

    def __init__(self,configfile,configpart):

        cf=ConfigParser.ConfigParser()

        cf.read(configfile)

        host=cf.get(configpart,"host")

        port = cf.get(configpart, "port")

        username = cf.get(configpart, "username")

        password = cf.get(configpart, "password")

        host = cf.get(configpart, "host")

        database = cf.get(configpart, "database")

        self.failPrint = cf.get(configpart, "failPrint")

        self.successPrint = cf.get(configpart, "successPrint")

        try:

            self.conn = pymysql.connect(
                    host=host,
                user=username, password=password,
                database=database, port=int(port),
                charset="utf8")

        except Exception as e:

            print(traceback.format_exc())

            print("mysql datasource string is:{"+"host:"+host+","+"port:"+port+","+"username:"+username+","+"password:"+password+","+"database:"+database+"}")

            sys.exit(1)


    def execSqlCmd(self,sql):

        try:

            errcode = 0

            data = []

            print("sql command is:"+"{" + sql + "}")

            cursor = self.conn.cursor()

            sqllist = sql.split(";")

            sqllist.remove("")

            for sql in sqllist:

                cursor.execute(sql)

                data.append(cursor.fetchall())

        except Exception as e:

            print(traceback.format_exc())

            data=self.failPrint

            errcode=999

            print(data)

        finally:

            self.conn.commit()

            cursor.close()

            if errcode == 0:

                print(self.successPrint)

            return data





class redisclient(databseclient):

    def __init__(self,configfile,configpart):

        cf=ConfigParser.ConfigParser()

        cf.read(configfile)

        host=cf.get(configpart,"host")

        port = cf.get(configpart, "port")

        username = cf.get(configpart, "username")

        password = cf.get(configpart, "password")

        database = cf.get(configpart, "database")

        self.excludeList = eval(cf.get(configpart, "excludeList"))

        self.failPrint = cf.get(configpart, "failPrint")

        self.successPrint = cf.get(configpart, "successPrint")

        try:

            self.redisClient = redis.StrictRedis(host=host, port=int(port), db=int(database))

        except Exception as e:

            print(traceback.format_exc())

            print("redis datasource string is:{"+"host:"+host+","+"port:"+port+","+"username:"+username+","+"password:"+password+","+"database:"+database+"}")

            sys.exit(1)


    def deleteallkeys(self):

        print("start to delete all keys......")

        for name in self.redisClient.keys("*"):

            if not (name in self.excludeList):

                self.redisClient.delete(name)

                print("delete key:" + str(name))


    def execRedisCmd(self,cmd):

        try:

            errcode = 0

            data=self.successPrint

            #if cmd == "deleteallkeys":

            getattr(self,cmd)()

        except Exception as e:

            print(traceback.format_exc())

            data=self.failPrint

            errcode=999

            print(data)

        finally:

            if errcode == 0:

                print(self.successPrint)

            return data


if __name__ == '__main__':

    myclient=mysqlclient("config.cfg","mysql")

    sql1="delete from test2;delete from test1;"

    myclient.execSqlCmd(sql1)

    # redisclient=redisclient("config.cfg","redis")
    #
    # redisclient.execRedisCmd("deleteallkeys")