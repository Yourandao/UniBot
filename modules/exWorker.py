import os
import re
import math
import datetime

import pandas
import openpyxl as xlReader
import requests

#----------------------------------

C_EN_ALPHABET_CAP = 26 
C_ASCII_A_KEY = 65
C_EXCEL_WEEK_LEN = 73
C_DAY_SUBJS = 12

A_WEEK_DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']

#----------------------------------

class WorkDay:
    subjects = []

    def __init__(self, rowsArr, dayIndex):
        self.subjects = rowsArr.copy()
        self.dayIndex = dayIndex

    #Get a even day shedule which one is nonspace string
    def GetEven(self):
        rString = '\n, '

        return A_WEEK_DAYS[self.dayIndex] + ':\n' + rString.join(
            [str(i // 2 + 1) + ' пара: ' + str(self.subjects[i]).replace('\n', '')
                for i in range(0, len(self.subjects), 2) if not str(self.subjects[i]).isspace()]
            ).replace(',' , '').replace('*', ' ')

    #Get a odd day shedule which one is nonspace string
    def GetOdd(self):
        rString = '\n, '

        return A_WEEK_DAYS[self.dayIndex] + ':\n' + rString.join(
            [str(i // 2 + 1) + ' пара: ' + str(self.subjects[i]).replace('\n', '')
                for i in range(1, len(self.subjects), 2) if not str(self.subjects[i]).isspace()]
            ).replace(',', '').replace('*', ' ')


class ExWorker:
    curGroup = ''

    def __init__(self, exFile):
        self.sheetName = 'Лист1'
        self.coordinates = tuple()
        
        self.exFile = exFile
        self.xlsx = xlReader.load_workbook('./shedules/' + exFile)
        self.mainSheet = self.xlsx.get_sheet_by_name(str(self.sheetName))
        self.data = list(self.mainSheet.values)
        self.workDays = []
        

    def ParseIfExist(self, group):
        for iRow in range(len(self.data)):
            for jCol in range(len(self.data[iRow])):
                if(str(self.data[iRow][jCol]).startswith(group)):

                    self.curGroup = group
                    self.coordinates = iRow, jCol, self.CoordToKey(jCol, iRow)

                    self.SetWeek()

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
        dayCount = 0

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

                self.workDays.append(WorkDay(subjRows, dayCount))
                subjRows.clear()

                dayCount += 1
    
    def GetWeek(self):
        curWeek = self.GetWeekNumber() % 2

        weekShedule = []

        for dayIndex in range(len(self.workDays)):
            dayResult = A_WEEK_DAYS[dayIndex] + ':\n'

            for i in range((0  if curWeek == 0 else 1), len(self.workDays[dayIndex].subjects), 2):
                if not str(self.workDays[dayIndex].subjects[i]).isspace():
                    dayResult += str((i + 1) // 2 + (1 if curWeek == 0 else 0)) + ' пара: ' + str(self.workDays[dayIndex].subjects[i]).replace('\n', '') + '\n'
            
            weekShedule.append(dayResult)
            dayResult = ''
        
        return '\n'.join(weekShedule).replace(',', '')

    def GetDay(self, day):
        for i in range(len(self.workDays)):
            if A_WEEK_DAYS[i] == str(day).lower():
                return self.workDays[i].GetEven() if self.GetWeekNumber() % 2 != 0 else self.workDays[i].GetOdd() # Don`t Touch
                
        return 'Пары не найдены'

    def GetNext(self):
        curDay = datetime.datetime.today().weekday()
        nextDay = (curDay + 1) % len(self.workDays)

        if nextDay + 1 != 6:
            return self.workDays[nextDay].GetEven() if self.GetWeekNumber() % 2 != 0 else self.workDays[nextDay].GetOdd()
        else:
            return 'Пары не найдены'

    def GetBack(self):
        curDay = datetime.datetime.today().weekday()

        if curDay == 0:
            curDay = 6
        
        return self.workDays[curDay - 1].GetEven() if self.GetWeekNumber() % 2 != 0 else self.workDays[curDay - 1].GetOdd()

    def GetToday(self):
        curDay = datetime.datetime.today().weekday()

        if curDay != 6:
            return self.workDays[curDay].GetEven() if self.GetWeekNumber() % 2 != 0 else self.workDays[curDay].GetOdd()
        else:
            return 'Пары не найдены'

    def GetWeekNumber(self):
        response = requests.get('https://www.mirea.ru/').text

        try:
            return int(re.search(r'<div class=\"date_text uk-display-inline-block\">\n.*?идет (\d{1,2})-я неделя.*?<\/div>', response).group(1))
        except:
            return -1