import os
import json
import discord
from discord.ext import commands

class Sheduler:
    memberList = {}

    def __init__(self, dClient):
        self.dClient = dClient

        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json'), 'r') as jFile:
            self.memberList = json.load(jFile)
    
    @commands.command(pass_context = True)
    async def setGroup(self, request, group : str):
        self.memberList[str(request.message.author)] = group

        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json'), 'w') as jFile:
            json.dump(self.memberList, jFile)

    @commands.command(pass_context = True)
    async def getGroup(self, request):
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json'), 'r') as jFile:
            self.memberList = json.load(jFile)

        await self.dClient.say(self.memberList[str(request.message.author)])


def setup(dClient):
    dClient.add_cog(Sheduler(dClient))