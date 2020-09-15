# -*- coding:utf-8 -*-

"""

    Created by liuyi.shen

    Created on 2020/7/14

"""

import ConfigParser
import codecs
import datetime
import sys
import shutil
import os
import time
import traceback
import xlrd

import clearDir
import searchFile


def compareExcel(config,configpart):

    try:

        cf = ConfigParser.ConfigParser()

        cf.read(config)

        ex1 = cf.get(configpart,"dataExpect").decode("utf-8")

        ex2 = cf.get(configpart, "dataFact").decode("utf-8")

        ex3 = cf.get(configpart, "dataFactBak").decode("utf-8")


        # if os.path.exists(ex3):
        #
        #     os.remove(ex3)
        #
        # shutil.copy(ex2,ex3)
        #
        # if os.path.exists(ex2):
        #
        #     os.remove(ex2)
        #
        # ex2=ex2

        failPrint = cf.get(configpart, "failPrint")

        successPrint = cf.get(configpart, "successPrint")


        sheetnum = cf.get(configpart, "sheetnum")

        outputfile = cf.get(configpart, "outputfile")

        sleepTime = int(cf.get(configpart, "sleepTime"))

        if sleepTime != "":

            time.sleep(sleepTime)


        if "," in ex2 and "$" in ex2:

            file2Path=ex2.split(",")[0]

            fileKeys=ex2.split(",")[1].split("$")[1:]

            ret=searchFile.searchFile(file2Path,fileKeys)

            if ret[0] != 0:

                print("failed to search file:" + str(ex2))

                print(failPrint)

                sys.exit(0)

            else:

                ex2=os.path.join(file2Path,ret[1])


        print("expect excel:" + ex1)

        print("fact excel:" + ex2)


        dataExpect = xlrd.open_workbook(ex1)

        dataExport = xlrd.open_workbook(ex2)

        f1=codecs.open(outputfile,'w','utf-8')


        if len(dataExpect.sheets()) != int(sheetnum):

            print("expect excel sheets number dose not match config sheets number;expect excel sheets number:" + str(len(dataExpect.sheets())) +";" + "config sheets number:" + str(sheetnum))

            print(failPrint)

            sys.exit(0)

        if len(dataExport.sheets()) != int(sheetnum):

            print("fact excel sheets number dose not match config sheets number;fact excel sheets number:" + str(len(dataExpect.sheets())) +";" + "config sheets number:" + str(sheetnum))

            print(failPrint)

            sys.exit(0)

        errcode=0

        for i in range(int(sheetnum)):

            table1 = dataExpect.sheets()[i]

            table2 = dataExport.sheets()[i]

            nrows1 = table1.nrows

            nrows2 = table2.nrows

            ncols1 = table1.ncols

            ncols2 = table2.ncols

            if nrows1 != nrows2:

                print("expect excel sheet no." + str(i+1) + " row number does not match fact excel row number;expect excel row number:" + str(
                    nrows1) + ";" + "fact excel row number:" + str(nrows2))

                print(failPrint)

                sys.exit(0)

            if ncols1 != ncols2:

                print("expect excel sheet no." + str(i+1) +  " column number does not match fact excel column number;expect excel column number:" + str(
                    ncols1) + ";" + "fact excel column number:" + str(ncols2))

                print(failPrint)

                sys.exit(0)

            for j in range(1,nrows1):

                for k in range(ncols1):


                    cell1=table1.cell_value(j, k)

                    cell2=table2.cell_value(j, k)

                    cell1Date=cell1

                    cell2Date = cell2

                    # cell1=valueToDateTime(cell1)
                    #
                    # cell2=valueToDateTime(cell2)

                    if (type(cell1) is int) or (type(cell1) is float):

                        cell1 = str(cell1)

                    elif (type(cell1) is datetime.datetime):

                        cell1 = str(cell1)

                    else:

                        cell1 = cell1.encode('utf-8')

                    if (type(cell2) is int) or (type(cell2) is float):

                        cell2 = str(cell2)

                    elif (type(cell2) is datetime.datetime):

                        cell2 = str(cell2)

                    else:

                        cell2 = cell2.encode('utf-8')

                    if cell1 != cell2:

                        errcode=999

                        if (valueToDateTime(cell1Date)[0] != 0 and valueToDateTime(cell2Date)[0] != 0):

                            f1.write("expect sheet no." + str(i+1) + " cell[" + str(j+1) + "," + str(k+1) + "]" + " does not match fact excel cell value;expect cell value:" +
                                cell1 + ";" + "fact cell value:" + cell2 + "\n")

                        else:

                            f1.write("expect sheet no." + str(i + 1) + " cell[" + str(j + 1) + "," + str(
                                k + 1) + "]" + " does not match fact excel cell value;expect cell value:" +
                                    cell1 + ";" + "fact cell value:" + cell2 + ";" + "if datetime, expect cell value:" +
                                        valueToDateTime(cell1Date)[1] + ";" + "if datetime, fact cell value:" + valueToDateTime(cell2Date)[1] + "\n")


        if errcode != 0:

            print("expect excel does not match fact excel,pls look up detail in " + outputfile)

            print(failPrint)

            sys.exit(0)

        else:

            print(successPrint)

        if f1:

            f1.close()

    except Exception as e:

        print(traceback.format_exc())

        print(failPrint)

        if f1:

            f1.close()

        sys.exit(0)

def valueToDateTime(cellValue):

    try:

        flag = 0

        cellValueNew = str(xlrd.xldate.xldate_as_datetime(cellValue,""))

    except Exception as e:

        # print(traceback.format_exc())

        flag = 9

        cellValueNew=cellValue

    finally:

        return [flag,cellValueNew]


if __name__ == '__main__':

    config = sys.argv[1]

    configPart = sys.argv[2]

    # config="config.cfg"
    #
    # configPart="excel"

    compareExcel(config, configPart)

    print valueToDateTime(0.3)



