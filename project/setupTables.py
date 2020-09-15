# -*- coding:utf-8 -*-

"""

    Created by liuyi.shen
    
    Created on 2020/7/13
          
"""

import ConfigParser

import sys
import time

import traceback

from databseclient import mysqlclient, redisclient


def setupTables(configfile, configpart):
    try:

        print("read config file:<" + configfile + "> and get config part:<" + configpart + ">")

        cf = ConfigParser.ConfigParser()

        cf.read(configfile)

        type = cf.get(configpart, "type")

        sqllist = cf.get(configpart, "sqllist")

        failPrint = cf.get(configpart, "failPrint")

        sqllist = sqllist.split(",")

        dbconfig = cf.get(configpart, "dbconfig")

        dbconfigpart = cf.get(configpart, "dbconfigpart")

        cf.read(dbconfig)

        dbfailPrint = cf.get(dbconfigpart, "failPrint")

    except Exception as e:

        print(traceback.format_exc())

        print("failed to get config!!!!!")

        print(failPrint)

        sys.exit(1)

    if type == "mysql":
        myclient = mysqlclient(dbconfig, dbconfigpart)

    if type == "redis":
        myclient = redisclient(dbconfig, dbconfigpart)

    for sql in sqllist:

        # print("sql config name:" + sql)

        try:

            sqlx = cf.get(configpart, sql)

        except Exception as e:

            print(traceback.format_exc())

            print("failed to get config of sql!!!!!")

            print(failPrint)

            sys.exit(1)

        if type == "mysql":
            x = myclient.execSqlCmd(sqlx)

        if type == "redis":
            x = myclient.execRedisCmd(sqlx)

        if dbfailPrint in x:

            print(failPrint)

            sys.exit(0)

    if type == "mysql":

        myclient.conn.close()


if __name__ == '__main__':

    setupTables("config.cfg", "setup_mysql")

    setupTables("config.cfg", "setup_redis")
