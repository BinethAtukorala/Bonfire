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
        Check whether the bot is online and see it's ping
        """

        await ctx.send(embed=discord.Embed(title="Pong! 🏓", description="`{}ms`".format(int(self.bot.latency * 100))))
    
    @commands.command(name="help")
    async def help(self, ctx):
        """
        Help command for the bot.
        """
        _, PREFIX = utils.get_discord_config()
        embed = discord.Embed(
            title=f"❔ Help - Bonfire",
            description=f"🎧 A Discord bot that enables you to listen along to your friends' Spotify tracks in real time.\n\n**Prefix** - `{PREFIX}`"
            ).add_field(
                name="⌨  Commands",
                value=f"\n▫**`{PREFIX}pair <optional user ID>`**  : Pair the bot to a user and start listening to his Spotify activity\n\n▫**`{PREFIX}unpair`**: Unpair from the currently paired user.\n\n▫**`{PREFIX}start`**: Start playing paired user's Spotify music.\n\n▫**`{PREFIX}stop`**    : Stop music playback\n",
                inline=False
            ).add_field(
                name="🤔  How to use the bot",
                value=f"\nEnter the `{PREFIX}pair` command to make the bot listen to\na user's Spotify activity.\n\nAfter that use the `{PREFIX}start` to\nmake the bot join the voice channel you are in and play music.\n\nUse the `{PREFIX}stop` command to stop the bot playing music.\n\nUse the `{PREFIX}unpair` command to stop the bot listening\nto the paired user's Spotify actvity."
            ).set_thumbnail(
                url="https://cdn.discordapp.com/attachments/864003637368717312/864426322989678642/cartoon-fire-flames-campfire_284092-1327.jpg",

        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MainCog(bot))