# -*- coding:utf-8 -*-

"""

    Created by liuyi.shen
    
    Created on 2020/7/9
          
"""

import ConfigParser
import codecs
import shutil
import os
import sys
import time
import traceback
import searchFile



def compareFile(config,configpart):

    try:

        cf = ConfigParser.ConfigParser()

        cf.read(config)

        file1 = cf.get(configpart, "file1").decode("utf-8")

        file2 = cf.get(configpart, "file2").decode("utf-8")

        file3 = cf.get(configpart, "file3").decode("utf-8")

        file4 = cf.get(configpart, "file4").decode("utf-8")

        failPrint = cf.get(configpart, "failPrint")

        successPrint = cf.get(configpart, "successPrint")

        sleepTime = int(cf.get(configpart, "sleepTime"))

        if sleepTime != "":

            time.sleep(sleepTime)

        if "," in file2 and "$" in file2:

            file2Path=file2.split(",")[0]

            fileKeys=file2.split(",")[1].split("$")[1:]

            ret=searchFile.searchFile(file2Path,fileKeys)

            if ret[0] != 0:

                print("failed to search file:" + str(file2))

                print(failPrint)

                sys.exit(0)

            else:

                file2=os.path.join(file2Path,ret[1])

        if os.path.exists(file4):

            os.remove(file4)

        shutil.copy(file2,file4)

        # if os.path.exists(file2):
        #
        #     os.remove(file2)

        file2=file2

        print("expect file:" + file1)

        print("fact file:" + file2)

        f1=codecs.open(file1,'r')

        f2=codecs.open(file2, 'r')

        f3=codecs.open(file3, 'w')

        list1=[]

        list2=[]

        for line1 in f1:

            list1.append(line1.strip("\n"))

        for line2 in f2:

            list2.append(line2.strip("\n"))

        err_flag=0

        tmpDict1={}

        i=0

        for str1 in list1:

            i=i+1

            if str1 in tmpDict1:

                err_flag = 1

                f3.write("file:" + file1 + " line no." + str(i) + " same as" + " line no." + str(tmpDict1[str1]) + "\n")

            else:

                tmpDict1[str1]=i

            if str1 in list2:

                pass

            else:

                err_flag=1

                f3.write("file:" + file1 + " line no." + str(i) + " not found in " + file2 + "\n")

        tmpDict1={}

        i=0

        for str1 in list2:

            i = i + 1

            if str1 in tmpDict1:

                err_flag = 1

                f3.write("file:" + file2 + " line no." + str(i) + " same as" + " line no." + str(tmpDict1[str1]) + "\n")

            else:

                tmpDict1[str1] = i

            if str1 in list1:

                pass

            else:

                err_flag = 1

                f3.write("file:" + file2 + " line no." + str(i) + " not found in " + file1 + "\n")



        if err_flag != 0:

            print("expect file does not match fact file,pls look up detail in " + file3)

            print(failPrint)

            sys.exit(0)

        else:

            print(successPrint)

            sys.exit(0)

        if f1:

            f1.close()

        if f2:

            f2.close()

        if f3:

            f3.close()


    except Exception as e:

        print(traceback.format_exc())

        print(failPrint)

        if f1:

            f1.close()

        if f2:

            f2.close()

        if f3:

            f3.close()

        sys.exit(0)


if __name__ == '__main__':

    config=sys.argv[1]

    configPart=sys.argv[2]

    # config="config.cfg"
    #
    # configPart="file2"

    compareFile(config, configPart)

