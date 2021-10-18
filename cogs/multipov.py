from twitchio.ext import commands


class Multipov(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="multipov", aliases=[])
    async def multipov(self, ctx: commands.bot.Context):
        channels = '/'.join(self.bot.multipov_channels)
        await ctx.send(f'https://kadgar.net/live/{ctx.author.channel.name}/{channels}')

    @commands.command(name="multiadd", aliases=[])
    async def multiadd(self, ctx: commands.bot.Context, *channels):
        if ctx.author.is_mod:
            for channel in channels:
                self.bot.multipov_channels.append(channel)
            await ctx.send('Multi mis à jour SeemsGood')

    @commands.command(name="multiset", aliases=[])
    async def multiset(self, ctx: commands.bot.Context, *channels):
        if ctx.author.is_mod:
            self.bot.multipov_channels = []
            for channel in channels:
                self.bot.multipov_channels.append(channel)
            await ctx.send('Multi mis à jour SeemsGood')

    @commands.command(name="multireset", aliases=[])
    async def multireset(self, ctx: commands.bot.Context):
        if ctx.author.is_mod:
            self.bot.multipov_channels = []
            await ctx.send('Multi a été reset SwiftRage')


def prepare(bot: commands.Bot):
    bot.add_cog(Multipov(bot))
