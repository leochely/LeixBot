import datetime

from twitchio.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ban")
    async def ban(self, ctx: commands.Context, user, reason="rise of the machines"):
        await ctx.send(f"/ban {user} {reason}")
        await ctx.send(f"Au revoir {user} HeyGuys")

    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user):
        await ctx.send(f"/unban {user}")
        await ctx.send(f"Bon retour parmi nous {user} HeyGuys !")

    @commands.command(name="leixban")
    async def leixban(self, ctx: commands.Context, user):
        await ctx.send(f"Non t'abuses {ctx.author.name}, on va pas ban {user} quand meme BibleThump")

    @commands.command(name="bn")
    async def bn(self, ctx: commands.Context, *name):
        if not name:
            name = ctx.author.name
        else:
            name = name[0]
        await ctx.send(f'Bonne nuit @{name} <3')

    @commands.command(name="uptime")
    async def uptime_command(self, ctx: commands.bot.Context):
        stream = await self.bot.fetch_streams(user_logins=[ctx.author.channel.name])

        if len(stream) == 0:
            return await ctx.send("Il n'y a pas de live en cours :(")

        uptime = datetime.datetime.now() - stream[0].started_at
        await ctx.send(f"En ligne depuis {uptime} (oui c'est précis)")

    @commands.command(name="dblade")
    async def dblade(self, ctx: commands.Context):
        await ctx.send(f'Je te dedicace cette dblade {ctx.author.name}!')

    @commands.command(name="boubou")
    async def boubou(self, ctx: commands.Context):
        await ctx.send(f'Désolé @Lickers__!')

    @commands.command(name="fx")
    async def fx(self, ctx: commands.Context):
        await ctx.send('Kel bo fx')

    @commands.command(name="so")
    async def so(self, ctx: commands.Context):
        await ctx.send('yapadeso')

    @commands.command(name="porte")
    async def porte(self, ctx: commands.Context):
        await ctx.send("Vision d'artiste")

    @commands.command(name="den")
    async def den(self, ctx: commands.Context):
        await ctx.send('https://discord.gg/PEfEVWacgP')

    @commands.command(name="ref")
    async def ref(self, ctx: commands.Context):
        await ctx.send('glaref leix34Trigerred')

    @commands.command(name="cam")
    async def cam(self, ctx: commands.Context):
        await ctx.send('MET LA CAM')


def prepare(bot: commands.Bot):
    bot.add_cog(Misc(bot))
