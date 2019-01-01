import os
import re
import json
import discord
import modules.exWorker as exHandle
from discord.ext    import commands

class Sheduler:
    memberList = {}

    def __init__(self, dClient):
        self.dClient = dClient
        self.loadData()

        self.xWorker = exHandle.ExWorker('asda.xlsx')

    def loadData(self):
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json'), 'r') as jFile:
            self.memberList = json.load(jFile)
    
    def updateData(self):
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json'), 'w') as jFile:
            json.dump(self.memberList, jFile, indent = 4)
    
    @commands.command(pass_context = True)
    async def setGroup(self, request, group : str):
        if re.match(r'\b[А-Я]{4}\b-\d{2}-\d{2}', group):
            self.memberList[str(request.message.author)] = group
            self.updateData()

            await self.dClient.send_message(request.message.channel, 'Group successfully edit')
        else:
            await self.dClient.send_message(request.message.channel, 'Group is incorrect')

    @commands.command(pass_context = True)
    async def getGroup(self, request):
        self.loadData()

        await self.dClient.send_message(request.message.channel, '{0.message.author} is in {1}'.format(request, self.memberList[str(request.message.author)]))

    @commands.command(pass_context = True)
    async def week(self, request):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        await self.dClient.send_message(request.message.channel, group + '\n\n' + self.xWorker.GetWeek())

    @commands.command(pass_context = True)
    async def today(self, request):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        await self.dClient.send_message(request.message.channel, group + '\n\n' + self.xWorker.GetToday())

    @commands.command(pass_context = True)
    async def day(self, request, day):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        await self.dClient.send_message(request.message.channel, group + '\n\n' + self.xWorker.GetDay(day))

    @commands.command(pass_context = True)
    async def tomorrow(self, request):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        await self.dClient.send_message(request.message.channel, group + '\n\n' + self.xWorker.GetNext())

    @commands.command(pass_context = True)
    async def yesterday(self, request):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        await self.dClient.send_message(request.message.channel, group + '\n\n' + self.xWorker.GetBack())

    @commands.command(pass_context = True)
    async def wnumber(self, request):
        weekNumber = self.xWorker.GetWeekNumber()
        await self.dClient.send_message(request.message.channel, weekNumber if weekNumber != -1 else 'Error' )

def setup(dClient):
    dClient.add_cog(Sheduler(dClient))