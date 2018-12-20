import os
import discord
import pandas
import openpyxl       as xlReader
import modules.exfunc as modules

xlsx = xlReader.load_workbook('./asda.xlsx')

mainSheet = xlsx.get_sheet_by_name('Лист1')
data = list(mainSheet.values)

print(modules.exists(data, 'БСБО-09-17'))

# data.index('БСБО-09-17 09.03.02(КБ-3)')
# AW3
