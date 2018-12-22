import os
import pandas
import openpyxl as xlReader
import math

class exWorker:
    sheetName = 'Лист1'
    curGroup = ''

    def __init__(self, exFile):
        self.exFile = exFile
        self.xlsx = xlReader.load_workbook('./' + exFile)
        self.mainSheet = self.xlsx.get_sheet_by_name(str(self.sheetName))
        self.data = list(self.mainSheet.values)

    def Exists(self, group):
        for iRow in range(len(self.data)):
            for jCol in range(len(self.data[iRow])):
                if(str(self.data[iRow][jCol]).startswith(group)):
                    self.curGroup = group
                    return self.CoordToKey(jCol, iRow)

        return False

    def CoordToKey(self, jIndex, iIndex):
        if jIndex >= 26:
            remain = jIndex // 26
            first = chr(64 + remain)
            second = chr(65 + jIndex - remain * 26)
            return str(first) + str(second) + str(iIndex + 1)

        else:
            return str(chr(64 + jIndex)) + str(iIndex)

    