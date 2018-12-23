import os
import discord
import pandas
import openpyxl         as xlReader
import modules.exWorker as exHandle

worker = exHandle.exWorker('asda.xlsx')

worker.Exists('БСБО-09-17')
worker.SetWeek()

# worker.days[2].GetEven()
worker.GetWeek()

