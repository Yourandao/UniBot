import os

import pandas
import asyncio
import discord
import youtube_dl
import openpyxl         as xlReader
import modules.exWorker as exHandle

from discord.ext import commands

#-----------------------------------

dClient = commands.Bot(command_prefix = '$')

players = {}
queues   = {}

@dClient.event
async def on_ready():
    print('Logged in as ' + dClient.user.name + ' ' + dClient.user.id)

@dClient.command(pass_context = True)
async def join(request):
    channel = request.message.author.voice.voice_channel

    if str(channel) != 'None':
        await dClient.join_voice_channel(channel)
    else:
        print('Nobody in channel')

@dClient.command(pass_context = True)
async def leave(request):
    for client in dClient.voice_clients:
        if client.server == request.message.server:
            return await client.disconnect()

@dClient.command(pass_context = True)
async def play(request, url):
    server = request.message.server
    channel = request.message.author.voice.voice_channel

    if not dClient.is_voice_connected(server):
        if str(channel) != 'None':
            vc = await dClient.join_voice_channel(channel)
        else:
            print('Channel is empty')
    else:
        vc = dClient.voice_client_in(server)

    player = await vc.create_ytdl_player(url, after= lambda: checkQueue(server.id))
    players[server.id] = player

    player.start()

@dClient.command(pass_context = True)
async def pause(request):
    players[request.message.server.id].pause()

@dClient.command(pass_context = True)
async def resume(request):
    players[request.message.server.id].resume()

@dClient.command(pass_context = True)
async def stop(request):
    players[request.message.server.id].stop()

@dClient.command(pass_context = True)
async def queue(request, url):
    server = request.message.server
    voiceClient = dClient.voice_client_in(server)
    player = await voiceClient.create_ytdl_player(url, after = lambda: checkQueue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    
    await dClient.say('Video queued')

def checkQueue(serverID):
    if queues[serverID] != []:
        player = queues[serverID].pop(0)
        players[serverID] = player
        player.start()

#-----------------------------------

D_TOKEN = open('./stuff/D_TOKEN.txt', 'r').read()
dClient.run(D_TOKEN)
