from discord.ext import commands
import discord

from lib import utils

class MainCog(commands.Cog):
    """
    Handles main commands related to the bot
    """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.MissingAnyRole, commands.MissingRole)):
            await ctx.send("Sorry, you don't have the necessary permissions to run this command.")
    
    @commands.command(name="ping")
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        """
        Check whether the bot is online
        """

        await ctx.send("Pong! `{}ms` 🏓".format(int(self.bot.latency * 100)))

def setup(bot):
    bot.add_cog(MainCog(bot))