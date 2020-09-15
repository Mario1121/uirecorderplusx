# -*- coding:utf-8 -*-

"""

    Created by liuyi.shen
    
    Created on 2020/8/14
          
"""

import ConfigParser
import codecs
import os
import shutil
import sys
import time
import traceback
import zipfile
import xlrd
from pip._vendor import chardet

import clearDir
import searchFile


def unZipFile(file_name,unzip_path):

    zip_file = zipfile.ZipFile(file_name)

    # if os.path.isdir(unzip_path):
    #
    #     pass
    #
    # else:
    #
    #     os.mkdir(unzip_path)

    for names in zip_file.namelist():

        zip_file.extract(names, unzip_path)

    zip_file.close()


def compareZip(config,configpart):

    try:

        errcode = 0

        cf=ConfigParser.ConfigParser()

        cf.read(config)

        dataExpect=cf.get(configpart,"dataExpect").decode("utf-8")

        dataExpectUnzipPath = cf.get(configpart, "dataExpectUnzipPath")

        dataFact = cf.get(configpart, "dataFact").decode("utf-8")

        dataFactUnzipPath = cf.get(configpart, "dataFactUnzipPath")

        dataFactPathBak = cf.get(configpart, "dataFactPathBak")

        sheetnum = cf.get(configpart, "sheetnum")

        outputfile = cf.get(configpart, "outputfile").decode("utf-8")

        failPrint = cf.get(configpart, "failPrint")

        successPrint = cf.get(configpart, "successPrint")

        sleepTime = int(cf.get(configpart, "sleepTime"))


        if sleepTime != "":

            time.sleep(sleepTime)

        if "," in dataFact and "$" in dataFact:

            file2Path = dataFact.split(",")[0]

            fileKeys = dataFact.split(",")[1].split("$")[1:]

            ret = searchFile.searchFile(file2Path, fileKeys)

            if ret[0] != 0:

                print("failed to search file:" + str(dataFact))

                print(failPrint)

                sys.exit(0)

            else:

                dataFact = os.path.join(file2Path, ret[1])

        if os.path.exists(dataExpectUnzipPath):

            clearDir.clearDir(dataExpectUnzipPath,failPrint,successPrint)

        else:

            os.makedirs(dataExpectUnzipPath)


        if os.path.exists(dataFactUnzipPath):

            clearDir.clearDir(dataFactUnzipPath,failPrint,successPrint)

        else:

            os.makedirs(dataFactUnzipPath)



        if os.path.exists(dataFactPathBak):

            clearDir.clearDir(dataFactPathBak,failPrint,successPrint)

        else:

            os.makedirs(dataFactPathBak)

        unZipFile(dataExpect, dataExpectUnzipPath)

        unZipFile(dataFact, dataFactUnzipPath)

        list_expect = os.listdir(dataExpectUnzipPath)

        list_fact = os.listdir(dataFactUnzipPath)


        if len(list_expect) != len(list_fact):

            print("expect unzip file amounts does not match fact.")

            print("expect unzip file amounts:" + str(len(list_expect)) + ";" + "fact unzip file amounts:" + str(len(list_fact)))

            print(failPrint)

            sys.exit(0)

        fout = codecs.open(outputfile,'w')

        for file1 in list_expect:

            expectFileName = os.path.basename(file1)

            expectFile = os.path.join(dataExpectUnzipPath,expectFileName)

            factFile = os.path.join(dataFactUnzipPath,expectFileName)

            bakFile = os.path.join(dataFactPathBak,expectFileName)

            ret=compareExcel(expectFile, factFile, bakFile, sheetnum, fout)

            if ret != 0:

                errcode = 999

    except Exception as e:

        print(traceback.format_exc())

        errcode = 99999

    finally:

        if errcode != 0:

            print(failPrint)

            print('pls check log file:' + outputfile + ".")

        else:

            print(successPrint)

        sys.exit(0)



def compareExcel(ex1,ex2,ex3,sheetnum,fout):

    try:

        if os.path.exists(ex3):

            os.remove(ex3)

        shutil.copy(ex2,ex3)

        if os.path.exists(ex2):

            os.remove(ex2)

        ex2=ex3

        # print chardet.detect(ex1)
        #
        # print("expect excel:" + ex1.decode('gbk').encode('utf-8'))
        #
        # print("fact excel:" + ex2.decode('gbk').encode('utf-8'))

        dataExpect = xlrd.open_workbook(ex1)

        dataExport = xlrd.open_workbook(ex2)

        f1=fout



        if len(dataExpect.sheets()) != int(sheetnum):

            print("expect excel sheets number dose not match config sheets number;expect excel sheets number:" + str(len(dataExpect.sheets())) +";" + "config sheets number:" + str(sheetnum))

            # print(failPrint)

            errcode = 1

            return errcode

        if len(dataExport.sheets()) != int(sheetnum):

            print("fact excel sheets number dose not match config sheets number;fact excel sheets number:" + str(len(dataExpect.sheets())) +";" + "config sheets number:" + str(sheetnum))

            # print(failPrint)

            errcode = 1

            return errcode

        errcode=0

        for i in range(int(sheetnum)):

            table1 = dataExpect.sheets()[i]

            table2 = dataExport.sheets()[i]

            nrows1 = table1.nrows

            nrows2 = table2.nrows

            ncols1 = table1.ncols

            ncols2 = table2.ncols

            if nrows1 != nrows2:

                print("expect excel sheet no." + str(i) + " row number does not match fact excel row number;expect excel row number:" + str(
                    nrows1) + ";" + "fact excel row number:" + str(nrows2))

                f1.write("expect excel sheet no." + str(i) + " row number does not match fact excel row number;expect excel row number:" + str(
                    nrows1) + ";" + "fact excel row number:" + str(nrows2) + "\n")
                # print(failPrint)

                errcode = 2

            if ncols1 != ncols2:

                print("expect excel sheet no." + str(i) +  " column number does not match fact excel column number;expect excel column number:" + str(
                    ncols1) + ";" + "fact excel column number:" + str(ncols2))

                f1.write("expect excel sheet no." + str(i) +  " column number does not match fact excel column number;expect excel column number:" + str(
                    ncols1) + ";" + "fact excel column number:" + str(ncols2) + "\n")

                # print(failPrint)

                errcode = 3


            for j in range(0,nrows1):

                for k in range(ncols1):

                    cell1=table1.cell_value(j, k)

                    cell2=table2.cell_value(j, k)

                    if cell1 != cell2:

                        errcode = 4


                        cell1 = cell1.encode('utf-8')

                        cell2 = cell2.encode('utf-8')


                        f1.write("expect sheet no." + str(i+1) + " cell[" + str(j+1) + "," + str(k+1) + "]" + " does not match fact excel cell value;expect cell value:" +
                    cell1 + ";" + "fact cell value:" + str(cell2) + "\n")


        # if errcode != 0:
        #
        #     print("expect excel does not match fact excel,pls look up detail in " + outputfile)
        #
        #     print(failPrint)
        #
        #     sys.exit(0)
        #
        # else:
        #
        #     print(successPrint)
        #
        # if f1:
        #
        #     f1.close()

    except Exception as e:

        print(traceback.format_exc())

        errcode = 999

    finally:

        return errcode

        # sys.exit(0)




if __name__ == '__main__':

    config = sys.argv[1]

    configPart = sys.argv[2]

    # config = "config.cfg"
    #
    # configPart = "zip"

    compareZip(config, configPart)

