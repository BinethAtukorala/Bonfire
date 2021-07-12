import discord
from discord.ext import commands
from discord import Spotify
import asyncio

import pprint

import datetime
import requests

import os

import pafy, youtube_search

import base64

from lib import utils



class SpotifyCog(commands.Cog):
    """
    Spotify listen along commands and listeners
    """

    def get_token(self):
        spotifyConfigs = utils.get_spotify_config()

        client_creds = base64.b64encode(f"{spotifyConfigs[0]}:{spotifyConfigs[1]}".encode()).decode()

        token_url = "https://accounts.spotify.com/api/token"
        method = "POST"
        token_data = {
            "grant_type": "client_credentials"
        }
        token_headers = {
            "Authorization": f"Basic {client_creds}"
        }

        response = requests.post(token_url, data=token_data, headers=token_headers).json()

        self.auth_token = response["access_token"]

    def __init__(self, bot):
        self.bot = bot
        self.current_user = None
        self.stop = True
        self.alreadyListening = False
        self.currentTrackID = None

        self.auth_token = None

        self.get_token()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.MissingAnyRole, commands.MissingRole)):
            await ctx.send("Sorry, you don't have the necessary permissions to run this command.")

    @commands.command(name="pair")
    async def pair(self, ctx, *args, **kwargs):
        if(len(args) != 1):
            if(self.current_user):
                await ctx.send(f"**{self.current_user.name}** is already paired to the bot")
            else:
                self.current_user = ctx.author
                await ctx.send(f"Paired to {self.current_user.name}")
        else:
            if(self.current_user):
                await ctx.send(f"**{self.current_user.name}** is already paired to the bot")
            else:
                self.current_user = ctx.guild.get_member(int(args[0]))
                await ctx.send(f"Paired to {self.current_user.name}")

    
    @commands.command(name="unpair")
    async def unpair(self, ctx):
        if(self.current_user == ctx.author):
            self.current_user = None
            await ctx.send(f"**{ctx.author.name}** unpaired.")
        else:
            await ctx.send(f"**{ctx.author.name}** is not paired")

    @commands.command(name="start")
    async def start(self, ctx):
        self.stop = False
        if(not(self.alreadyListening)):
            alreadyListening = True
            asyncio.ensure_future(self.listen(ctx))       
        
        
    async def listen(self, ctx):
        while(not(self.stop) and (self.current_user != None)):
            for activity in self.current_user.activities:
                if isinstance(activity, Spotify):
                    if(self.currentTrackID != activity.track_id):
                        self.currentTrackID = activity.track_id

                        if ctx.message.author.voice == None:
                            await ctx.send("No Voice Channel")
                            return

                        channel = ctx.message.author.voice.channel

                        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
                        
                        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

                        if voice_client == None:
                            voice_client = await voice.connect()
                        else:
                            await voice_client.move_to(channel)

                        voice_client.stop()
                        
                        startTime = activity.start + datetime.timedelta(hours=5, minutes=30)
                        trackID = activity.track_id
                
                        response = requests.get(f"https://api.spotify.com/v1/tracks/{trackID}", headers={"Authorization":f"Bearer {self.auth_token}"})
                        spotifyTrackMetaData = response.json()

                        if('error' in spotifyTrackMetaData):
                            self.get_token()
                        else:

                            results = youtube_search.YoutubeSearch(f"{spotifyTrackMetaData['name']} {spotifyTrackMetaData['artists'][0]['name']}", max_results=5).to_dict()

                            vidID = None
                            difference = 100000000000000000000

                            for video in results:
                                tmpID = video["url_suffix"]
                                if (video["duration"] == utils.ms_to_minsec(spotifyTrackMetaData["duration_ms"])):
                                    diff = 0
                                    vidID = tmpID
                                    break
                                diff = abs(float(spotifyTrackMetaData["duration_ms"]) - utils.minsec_to_ms(video["duration"]))

                                print(f"Difference: { abs(float(spotifyTrackMetaData['duration_ms'])) } - { abs(utils.minsec_to_ms(video['duration']))} = {diff}")
                                if(diff < difference):
                                    difference = diff
                                    vidID = tmpID
                            print(vidID)
                            if(vidID != None):
                                song = pafy.new("https://www.youtube.com" + vidID)
                                audio = song.getbestaudio()
                                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
                                source = discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
                                voice_client.play(source)

                            break
            await asyncio.sleep(1)
        self.alreadyListening = False
    
    @commands.command(name="stop")
    async def stop(self, ctx):
        self.stop = True
        self.alreadyListening = False

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client != None:
            voice_client.stop()
            await voice_client.disconnect()
        await ctx.send("Stopped")

def setup(bot):
    bot.add_cog(SpotifyCog(bot))