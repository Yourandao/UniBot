import os
import discord
from discord.ext import commands

dClient = commands.Bot(command_prefix = '.')

extensions = ['modules.sheduler', 'modules.ytdlWorker']

#-----------------------------------

@dClient.event
async def on_ready():
    print('Logged in as ' + dClient.user.name + ' ' + dClient.user.id)    

#-----------------------------------
if __name__ == '__main__':
    for extension in extensions:
        try:
            dClient.load_extension(extension)
        except Exception as err:
            print('{} cannot be loaded [{}]'.format(extension, err))

    D_TOKEN = open('./stuff/D_TOKEN.txt', 'r').read()
    dClient.run(D_TOKEN)
