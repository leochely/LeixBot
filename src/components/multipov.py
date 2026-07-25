from twitchio import User
from twitchio.ext import commands

class Multipov(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot
        self.multipov_channels = {}

    @commands.command(name="multipov", aliases=[])
    async def multipov(self, ctx: commands.Context):
        """Renvoie le lien multipov. Ex: !multipov"""
        if ctx.broadcaster.id not in self.multipov_channels:
            self.multipov_channels[ctx.broadcaster.id] = []
        channels = '/'.join(self.multipov_channels[ctx.broadcaster.id])
        await ctx.send(f'https://kadgar.net/live/{ctx.author.channel.name}/{channels}')

    @commands.is_moderator()
    @commands.command(name="multiadd", aliases=[])
    async def multiadd(self, ctx: commands.Context, *channels: User):
        """Ajoute un streamer au lien multipov. Requiert privilege modérateur.
        Ex: !multiadd leix34
        """
        if ctx.broadcaster.id not in self.multipov_channels:
            self.multipov_channels[ctx.broadcaster.id] = []
        for channel in channels:
            self.multipov_channels[ctx.broadcaster.id].append(channel.name)
        await ctx.send('Multi mis à jour SeemsGood')

    @commands.is_moderator()
    @commands.command(name="multiset", aliases=[])
    async def multiset(self, ctx: commands.Context, *channels: User):
        """Regle le lien multipov sur les chaines choisies. Requiert privilege
        modérateur.
        Ex: !multiset chaine1 chaine2 ...
        """
        self.multipov_channels[ctx.broadcaster.id] = []
        for channel in channels:
            self.multipov_channels[ctx.broadcaster.id].append(channel.display_name)
        await ctx.send('Multi mis à jour SeemsGood')

    @commands.is_moderator()
    @commands.command(name="multireset", aliases=[])
    async def multireset(self, ctx: commands.Context):
        """Réinitialise le lien multipov. Requiert privilege modérateur.
        Ex: !multireset"""
        self.multipov_channels[ctx.broadcaster.id] = []
        await ctx.send('Multi a été reset SwiftRage')

async def setup(bot: commands.AutoBot):
    await bot.add_component(Multipov(bot))
