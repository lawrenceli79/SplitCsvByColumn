# This script split <csvFil> by 1st column
# This script was successfully tested on Python 3.7

import sys
import os
import re
import time
import datetime
import collections

if (len(sys.argv)<=1):
    str = ("Split large csv file(e.g. dbg.txt) by beginning column.\n"
            "Usage:\n"
            "   py {} <LogFile> <Options>\n"
            "Options:\n"
            "   /h    With header row\n"
            .format(os.path.basename(__file__))
    )
    print(str)
    sys.exit()

bHeader = False
strInFile = sys.argv[1]
for i in range(2,len(sys.argv)):
    strOption = sys.argv[i]
    strOptionl = strOption.lower()
    mo = re.match(r"/h", strOptionl) 
    if(mo):
        bHeader = True


class OutFileManager:
    dictFile = {}
    headerLine = ""
    
    def OpenInitFile(self, strOutFile:str):
        fOut = open(strOutFile, "w")
        if(self.headerLine!=""):
            fOut.write(self.headerLine)
        return fOut

    def WriteToFile(self, strOutFile:str, line:str):
        fOut = None
        if(strOutFile in self.dictFile):
            fOut = self.dictFile[strOutFile]
        else:
            fOut = self.OpenInitFile(strOutFile)
            self.dictFile[strOutFile] = fOut
        fOut.write(line)

    def CloseAll(self):
        for key, fOut in self.dictFile.items():
            fOut.close()


with open(strInFile, errors='ignore') as fIn:
    ofm = OutFileManager()
    for i,line in enumerate(fIn):
        if(bHeader and i==0):
            ofm.headerLine = line
        else:
            mo = re.match(r"^([^,]+),", line)
            if(mo!=None):
                col = mo.group(1)
                strOutFile = strInFile + "_" + col
                ofm.WriteToFile(strOutFile, line)
    ofm.CloseAll()
