import os
import pandas
import openpyxl as xlReader
import math
import re
import requests

C_EN_ALPHABET_CAP = 26
C_ASCII_A_KEY = 65
C_EXCEL_WEEK_LEN = 73
C_DAY_SUBJS = 12

class workDay:
    subjects = []

    def __init__(self, rowsArr):
        self.subjects = rowsArr.copy()

    def GetEven(self):
        [print(str(i // 2 + 1) + ' пара: ' + str(self.subjects[i]).replace('\n', ''))
            for i in range(0, len(self.subjects), 2) if not str(self.subjects[i]).isspace()]

    def GetOdd(self):
        [print(str(i // 2 + 1) + ' пара: ' + str(self.subjects[i]).replace('\n', ''))
            for i in range(1, len(self.subjects), 2) if not str(self.subjects[i]).isspace()]


class exWorker:
    sheetName = 'Лист1'
    curGroup = ''

    coordinates = tuple()

    workDays = []
    days = ['понедельник', 'пторник', 'среда', 'четверг', 'пятница', 'суббота']

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
                    self.coordinates = iRow, jCol, self.CoordToKey(jCol, iRow)

                    return True
        return False

    def CoordToKey(self, jIndex, iIndex):
        if jIndex >= C_EN_ALPHABET_CAP:
           
            remain = jIndex // C_EN_ALPHABET_CAP
            first = chr(C_ASCII_A_KEY - 1 + remain)
            second = chr(C_ASCII_A_KEY + jIndex - remain * C_EN_ALPHABET_CAP)
            
            return str(first) + str(second) + str(iIndex + 1)

        else:
            return str(chr(C_ASCII_A_KEY - 1 + jIndex)) + str(iIndex)


    def SetWeek(self):
        rowCount = 0

        subjRows = []
        for row in self.mainSheet[self.CoordToKey(self.coordinates[1], self.coordinates[0] + 2) :
                                        self.CoordToKey(self.coordinates[1] + 3, self.coordinates[0] + C_EXCEL_WEEK_LEN)]:
            sRow = ''
            for elem in row:
                if elem.value is None:
                    sRow += str(' ')
                else:
                    sRow += str(elem.value) + ' '
            
            rowCount += 1
            subjRows.append(sRow)

            if rowCount == C_DAY_SUBJS:
                rowCount = 0

                self.workDays.append(workDay(subjRows))
                subjRows.clear()

    
    def GetWeek(self):
        curWeek = self.GetWeekNumber() % 2

        for dayIndex in range(len(self.workDays)):
            print(self.days[dayIndex] + ':')

            for i in range((0  if curWeek == 0 else 1), len(self.workDays[dayIndex].subjects), 2):
                if not str(self.workDays[dayIndex].subjects[i]).isspace():
                    print(str((i + 1) // 2 + (1 if curWeek == 0 else 0)) + ' пара: ' + 
                        str(self.workDays[dayIndex].subjects[i]).replace('\n', ''))

            print('------------------------------------')
    
    def GetDay(self, day):
        for i in range(len(self.workDays)):
            if self.days[i] == str(day).lower():
                self.workDays[i].GetEven() if self.GetWeekNumber() != 0 else self.workDays[i].GetOdd() # Don`t Touch

                return True
                
        print('Пары не найдены')
        return False

    def GetWeekNumber(self):
        response = requests.get('https://www.mirea.ru/').text

        try:
            return int(re.search(r'<div class=\"date_text uk-display-inline-block\">\n.*?идет (\d{1,2})-я неделя.*?<\/div>', response).group(1))
        except:
            return -1