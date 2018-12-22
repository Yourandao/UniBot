import os
import discord
import pandas
import openpyxl         as xlReader
import modules.exWorker as exHandle

worker = exHandle.exWorker('asda.xlsx')
# print(worker.exists('БСБО-09-17'))

# for elem in worker.mainSheet['CD2:CG15']:
#     for el in elem:
#         if el.value is not None:
#             print(el.value)
#     print('----')

print(worker.Exists('БСБО-09-17'))


