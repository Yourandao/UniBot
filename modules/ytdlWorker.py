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

    @commands.command(pass_context = True)
    async def join(self, request):
        channel = request.message.author.voice.voice_channel

        if str(channel) != 'None':
            await self.dClient.join_voice_channel(channel)
        else:
            print('Nobody in channel')

    @commands.command(pass_context = True)
    async def leave(self, request):
        for client in self.dClient.voice_clients:
            if client.server == request.message.server:
                return await client.disconnect()

        return False

    @commands.command(pass_context = True)
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

    @commands.command(pass_context = True)
    async def pause(self, request):
        self.players[request.message.server.id].pause()
    
    @commands.command(pass_context = True)
    async def resume(self, request):
        self.players[request.message.server.id].resume()
    
    @commands.command(pass_context = True)
    async def stop(self, request):
        self.players[request.message.server.id].stop()

    @commands.command(pass_context = True)
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