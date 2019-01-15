import time

import discord
import youtube_dl
from discord.ext import commands

class YTDLWorker:
    players = {}
    queues  = {}

    #-------------------------------

    def __init__(self, dClient):
        self.dClient = dClient
    
    def checkQueue(self, serverID):
        if self.queues[serverID] != []:
            player = self.queues[serverID].pop(0)
            self.players[serverID] = player
            
            player.start()

    #-------------------------------

    @commands.command(pass_context = True, 
                      brief        = 'Join bot to channel', 
                      description  = 'Function joins bot to channel')
    async def join(self, request):
        channel = request.message.author.voice.voice_channel

        if str(channel) != 'None':
            await self.dClient.join_voice_channel(channel)
        else:
            print('Nobody in channel')

    @commands.command(pass_context = True, 
                      brief        = 'Leave bot to channel', 
                      description  = 'Function leave bot to channel')
    async def leave(self, request):
        for client in self.dClient.voice_clients:
            if client.server == request.message.server:
                return await client.disconnect()
        return False

    @commands.command(pass_context = True,
                      brief        = 'Show current audio title',
                      description  = 'Function shows now playing audio track')
    async def nowplaying(self, request):
        server = request.message.server

        embed = discord.Embed()

        embed.add_field(name = 'Author', value = self.players[server.id].uploader, inline = False)
        embed.add_field(name = 'Title',  value = self.players[server.id].title,    inline = False)
        embed.add_field(name = 'Duration', value = time.strftime('%M:%S', time.gmtime(self.players[server.id].duration)))

        await self.dClient.say(embed = embed)

    @commands.command(pass_context = True, 
                      brief        = 'Play current youtube url. Error can be with stream urls', 
                      description  = 'Function plays current youtube url. Error can be with stream url')
    async def play(self, request, url):
        server = request.message.server
        channel = request.message.author.voice.voice_channel

        if not self.dClient.is_voice_connected(server):
            if str(channel) != 'None':
                voiceClient = await self.dClient.join_voice_channel(channel)
            else:
                print('Channel id empty')
        else:
            voiceClient = self.dClient.voice_client_in(server)

        player = await voiceClient.create_ytdl_player(url, after = lambda: self.checkQueue(server.id))
        self.players[server.id] = player

        player.start()

    @commands.command(pass_context = True,
                      brief        = 'Pause current track',
                      description  = 'Function pauses current track')
    async def pause(self, request):
        self.players[request.message.server.id].pause()
    
    @commands.command(pass_context = True,
                      brief        = 'Resume current track',
                      description  = 'Function resumes current track')
    async def resume(self, request):
        self.players[request.message.server.id].resume()
    
    @commands.command(pass_context = True,
                      brief        = 'Stop current track',
                      description  = 'Function stops current track')
    async def stop(self, request):
        self.players[request.message.server.id].stop()

    @commands.command(pass_context = True,
                      brief        = 'Add input url to queue',
                      description  = 'Function adds input url to queue')
    async def queue(self, request, url):
        server = request.message.server
        voiceClient = self.dClient.voice_client_in(server)

        player = await voiceClient.create_ytdl_player(url, after = lambda: self.checkQueue(server.id))

        if server.id in self.queues:
            self.queues[server.id].append(player)
        else:
            self.queues[server.id] = [player]

        await self.dClient.say('Video queued')
    
    #-------------------------------    

def setup(dClient):
    dClient.add_cog(YTDLWorker(dClient))