import os
import re
import json
import discord
import datetime
import modules.exWorker as exHandle
from discord.ext    import commands

class Sheduler:
    memberList = {}
    
    #-------------------------------

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
    
    #-------------------------------

    @commands.command(pass_context = True, 
                      brief = 'Set your own group', 
                      description = 'Function sets your own group')
    async def setGroup(self, request, group : str):
        if re.match(r'\b[А-Я]{4}\b-\d{2}-\d{2}', group):
            self.memberList[str(request.message.author)] = group
            self.updateData()

            await self.dClient.send_message(request.message.channel, 'Group successfully edit')
        else:
            await self.dClient.send_message(request.message.channel, 'Group is incorrect')

    @commands.command(pass_context = True, 
                      brief = 'Return your group', 
                      description = 'Function returns your own group')
    async def getGroup(self, request):
        self.loadData()

        await self.dClient.send_message(request.message.channel, '{0.message.author} is in {1}'.format(request, self.memberList[str(request.message.author)]))

    @commands.command(pass_context = True, 
                      brief = 'Return shedule on all current week', 
                      description = 'Function returns shedule on all currect week')
    async def week(self, request):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        embed = discord.Embed(
            title = 'Расписание на неделю',
            colour = discord.Color.dark_green()
        ).add_field(name = group, value = self.xWorker.GetWeek())

        await self.dClient.say(embed = embed)

    @commands.command(pass_context = True, 
                      brief = 'Return shedule on current day', 
                      description = 'Function returns shedule on current day')
    async def today(self, request):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        embed = discord.Embed(
            title = 'Расписание на сегодня',
            colour = discord.Color.dark_red()
        ).add_field(name = group, value = self.xWorker.GetToday())

        await self.dClient.say(embed = embed)

    @commands.command(pass_context = True, 
                      brief = 'Return shedule on input day',
                      description = 'Function returns shedule on input day')
    async def day(self, request, day):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        embed = discord.Embed(
            title = 'Расписание на {0}'.format(day),
            colour = discord.Color.orange()
        ).add_field(name = group, value = self.xWorker.GetDay(day))

        await self.dClient.say(embed = embed)

    @commands.command(pass_context = True, 
                      brief = 'Return shedule on next day', 
                      description = 'Function returns shedule on next day')
    async def tomorrow(self, request):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        embed = discord.Embed(
            title = 'Расписание на {0}'.format(exHandle.A_WEEK_DAYS[(datetime.datetime.today().weekday() + 1) % 7]),
            colour = discord.Color.darker_grey()
        ).add_field(name = group, value = self.xWorker.GetNext())

        await self.dClient.say(embed = embed)

    @commands.command(pass_context = True, 
                      brief = 'Return shedule on past day', 
                      description = 'Function returns shedule on past day')
    async def yesterday(self, request):
        self.loadData()

        group = self.memberList[str(request.message.author)]
        self.xWorker.ParseIfExist(group)

        current = datetime.datetime.today().weekday()

        embed = discord.Embed(
            title = 'Расписание на {0}'.format(exHandle.A_WEEK_DAYS[current - 1 if current != 0 else 6]),
            colour = discord.Colour.dark_teal()
        ).add_field(name = group, value = self.xWorker.GetBack())

        await self.dClient.say(embed = embed)

    @commands.command(pass_context = True, 
                      brief = 'Return number of current week', 
                      description = 'Function returns number of current week')
    async def wnumber(self, request):
        
        weekNumber = self.xWorker.GetWeekNumber()
        await self.dClient.send_message(request.message.channel, weekNumber if weekNumber != -1 else 'Error' )

    #-------------------------------

def setup(dClient):
    dClient.add_cog(Sheduler(dClient))