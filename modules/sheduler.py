import discord
from discord.ext import commands

class Sheduler:
    memberList = []

    def __init__(self, dClient):
        self.dClient = dClient
    # @commands.command(pass_context = True)
    # async def setGroup(self, )

    async def on_message_delete(self, message):
        await self.dClient.send_message(message.channel, 'Message deleted')


def setup(dClient):
    dClient.add_cog(Sheduler(dClient))