import os

from twitchio.ext import commands


class Multipov(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.multipov_channels = {
            x.name: [] for x in self.bot.connected_channels
        }

    @commands.command(name="multipov", aliases=[])
    async def multipov(self, ctx: commands.bot.Context):
        """Renvoie le lien multipov. Ex: !multipov"""
        channels = '/'.join(self.multipov_channels[ctx.author.channel.name])
        await ctx.send(f'https://kadgar.net/live/{ctx.author.channel.name}/{channels}')

    @commands.command(name="multiadd", aliases=[])
    async def multiadd(self, ctx: commands.bot.Context, *channels):
        """Ajoute un streamer au lien multipov. Requiert privilege modérateur.
        Ex: !multiadd leix34
        """
        if ctx.author.is_mod:
            for channel in channels:
                self.multipov_channels[ctx.author.channel.name].append(channel)
            await ctx.send('Multi mis à jour SeemsGood')

    @commands.command(name="multiset", aliases=[])
    async def multiset(self, ctx: commands.bot.Context, *channels):
        """Regle le lien multipov sur les chaines choisies. Requiert privilege
        modérateur.
        Ex: !multiset chaine1 chaine2 ...
        """
        if ctx.author.is_mod:
            self.multipov_channels[ctx.author.channel.name] = []
            for channel in channels:
                self.multipov_channels[ctx.author.channel.name].append(channel)
            await ctx.send('Multi mis à jour SeemsGood')

    @commands.command(name="multireset", aliases=[])
    async def multireset(self, ctx: commands.bot.Context):
        """Réinitialise le lien multipov. Requiert privilege modérateur.
        Ex: !multireset"""
        if ctx.author.is_mod:
            self.multipov_channels[ctx.author.channel.name] = []
            await ctx.send('Multi a été reset SwiftRage')


def prepare(bot: commands.Bot):
    bot.add_cog(Multipov(bot))
