# -*- coding:utf-8 -*-

"""

    Created by liuyi.shen
    
    Created on 2020/8/13
          
"""

import os
import shutil
import sys
import traceback


def clearDir(filepath,failPrint,successPrint):

    try:

        filepath=filepath
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    except Exception as e:

        print(traceback.format_exc())

        print(failPrint)


if __name__ == '__main__':

    failPrint = "failed to clear directory."

    successPrint = "succeed to clear directory."

    filepath=sys.argv[1]

    clearDir(filepath,failPrint,successPrint)


