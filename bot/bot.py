import discord
from discord.ext import commands


class BonfireBot(commands.Bot):

    COGS = [
        'bot.cogs.main',
        'bot.cogs.spotify'
    ]

    def __init__(self, token, prefix):
        self.TOKEN = token
        self.PREFIX = prefix

        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True


        super().__init__(
            command_prefix=prefix,
            description="Listen to Spotify along with your friends...",
            intents=intents
        )

        for cog in self.COGS:
            try:
                self.load_extension(cog)
            except Exception as e:
                raise Exception("Failed to load cog {}".format(cog))

    async def on_ready(self):
        printStr = "\nLogged in as:\n"
        printStr += f"Username: {self.user.name}#{self.user.discriminator}\n"
        printStr += f"ID: {self.user.id}\n\n"
        printStr += "Connected to servers:"

        guilds = await self.fetch_guilds(limit=100).flatten()
        for guild in guilds:
            printStr += f"\n* {guild.name}"

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"{self.PREFIX}help")    
        )
    
    def run(self):
        super().run(self.TOKEN, reconnect=True)