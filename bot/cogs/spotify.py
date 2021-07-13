# Discord Imports

import discord
from discord.ext import commands
from discord import Spotify
import asyncio

# Other imports

import datetime
import requests

import os

import pafy, youtube_search

import base64

from lib import utils



class SpotifyCog(commands.Cog):
    """
    Spotify listen along, commands and listeners
    """

    def get_token(self):
        """
        Refresh Spotify API Token
        """

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
            await ctx.send(embed=discord.Embed(title="⚠  No Permissions", description="Sorry, you don't have the necessary permissions to run this command."))

    @commands.command(name="pair")
    async def pair(self, ctx, *args, **kwargs):
        """
        Pair with a user to listen to his Spotify activity.
        """
        if(self.current_user):
            await ctx.send(embed=discord.Embed(title="👌  Already paired", description=f"**{self.current_user.name}** is already paired to the bot"))
        else:
            if(len(args) != 1):
                self.current_user = ctx.author

            else:
                self.current_user = ctx.guild.get_member(int(args[0]))
            
            await ctx.send(embed=discord.Embed(title="✅  Paired!", description=f"Paired to {self.current_user.name}"))

    
    @commands.command(name="unpair")
    async def unpair(self, ctx):
        """
        Unpair with currently paired user.
        """
        if(self.current_user != None):
            self.current_user = None
            await ctx.send(embed=discord.Embed(title="✅  Unpaired!", description=f"**{ctx.author.name}** unpaired."))
        else:
            await ctx.send(embed=discord.Embed(title="🤔  Not paired", description=f"**{ctx.author.name}** is not paired to be unpaired."))

    @commands.command(name="start")
    async def start(self, ctx):
        """
        Start playing Spotify tracks
        """
        self.stop = False
        if(not(self.alreadyListening)):
            if(self.current_user != None):
                alreadyListening = True
                await ctx.send(embed=discord.Embed(title="🎧  Started listening!", description=f"Started listening to, and playing **{self.current_user.name}**'s Spotify."))
                asyncio.ensure_future(self.listen(ctx))       
            else:
                await ctx.send(embed=discord.Embed(title="⛔  Not paired", description=f"No one is paired to be listened."))
        else:
            await ctx.send(embed=discord.Embed(title="🎧  Started listening!", description=f"Started listening to, and playing **{self.current_user.name}**'s Spotify."))
        
        
    async def listen(self, ctx):
        """
        Async function to playback music
        """
        while(not(self.stop) and (self.current_user != None)):
            for activity in self.current_user.activities:
                if isinstance(activity, Spotify):
                    if(self.currentTrackID != activity.track_id):
                        self.currentTrackID = activity.track_id

                        # Check if user is connected to a voice channel
                        if ctx.message.author.voice == None:
                            await ctx.send("No Voice Channel")
                            return

                        channel = ctx.message.author.voice.channel

                        voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
                        
                        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

                        # Connect to voice channel
                        if voice_client == None:
                            voice_client = await voice.connect()
                        else:
                            await voice_client.move_to(channel)

                        # Stop already playing track
                        voice_client.stop()
                        
                        startTime = activity.start + datetime.timedelta(hours=5, minutes=30)
                        trackID = activity.track_id

                        # Get Spotify track metadata
                        response = requests.get(f"https://api.spotify.com/v1/tracks/{trackID}", headers={"Authorization":f"Bearer {self.auth_token}"})
                        spotifyTrackMetaData = response.json()

                        print(1)

                        if('error' in spotifyTrackMetaData):
                            self.get_token()
                        else:
                            # Search Youtube for matching song
                            results = youtube_search.YoutubeSearch(f"{spotifyTrackMetaData['name']} {spotifyTrackMetaData['artists'][0]['name']}", max_results=3).to_dict()

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
                            # Play song if a proper match is found
                            if(vidID != None):
                                song = pafy.new("https://www.youtube.com" + vidID)
                                print(2)
                                audio = song.getbestaudio()
                                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
                                source = discord.FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
                                voice_client.play(discord.PCMVolumeTransformer(source, volume=0.5))

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
        await ctx.send(embed=discord.Embed(title="🔇  Stopped", description="Stopped listening to Spotify."))

def setup(bot):
    bot.add_cog(SpotifyCog(bot))