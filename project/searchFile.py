# -*- coding:utf-8 -*-

"""

    Created by liuyi.shen
    
    Created on 2020/8/13
          
"""
import ConfigParser
import datetime
import os
import sys
import traceback
import time

def getLatestFile(fileList):

    latestMTime = datetime.datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

    latestFile = ""

    for xfile in fileList:

        modifiedTime = time.localtime(os.stat(xfile).st_mtime)
        # createdTime = time.localtime(os.stat("D:/mm.cfg").st_ctime)

        mTime = time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)
        # cTime = time.strftime('%Y-%m-%d %H:%M:%S', createdTime)

        mTime = datetime.datetime.strptime(mTime, "%Y-%m-%d %H:%M:%S")

        if mTime >= latestMTime:

            latestMTime = mTime

            latestFile = xfile

    return latestFile

def searchFile(path,keys):

    try:

        path = path.decode("UTF-8")

        errcode=0

        filename=""

        fileList = []

        if os.path.exists(path):

            files = os.listdir(path)

            for f in files:

                flag = 0

                for key in keys:

                    if key in f:

                        pass

                    else:

                        flag = 1

                        break

                if flag == 0:

                    fileList.append(f)

                    # filename = f
                    # break


            if fileList:

                filename=getLatestFile(fileList)


        else:

            print("search path:" + "\"" + str(path) + "\"" + " does not exist!")

            errcode = 9

    except Exception as e:

        print(traceback.format_exc())

        errcode = 9

    finally:

        if filename == "":

            errcode = 9

        return [errcode,filename]

if __name__ == '__main__':

    # path="C:\\Users\\LIUYI\\Desktop\\赌博网站标注\\标注"
    #
    # key="SH-HLWB-IPTV-0023_check_report"
    #
    # print searchFile(path, key)
    #
    # str1="D:\\testdir\\,$x.txt$1"
    #
    # print(str1.split(",")[1].split("$"))
    #
    # print str1.split(",")[1].split("$")[1:]

    # config=sys.argv[1]
    #
    # configpart = sys.argv[2]
    #
    # cf=ConfigParser.ConfigParser()
    #
    # cf.read(config)
    #
    # x=cf.get(configpart,"file2")
    #
    # print x

    xfile="url.txt"

    modifiedTime = time.localtime(os.stat(xfile).st_mtime)

    mTime = time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)

    print modifiedTime

    print type(mTime)

    mTime2 = "2020-07-23 09:53:09"

    mTime = "2020-11-23 09:53:08"

    x1= datetime.datetime.strptime(mTime, "%Y-%m-%d %H:%M:%S")

    x2= datetime.datetime.strptime(mTime2, "%Y-%m-%d %H:%M:%S")

    if x1 > x2:

        print "y"