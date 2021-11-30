import datetime
import logging
import asyncio

from twitchio.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mh_id = "id not set!"

    @commands.command(name="discord")
    async def discord(self, ctx: commands.Context):
        await ctx.send("Le discord: https://discord.com/invite/jzU7xWstS9")

    @commands.command(name="ban")
    async def ban(self, ctx: commands.Context, user, reason="rise of the machines"):
        if ctx.author.is_mod or ctx.author.name == user:
            await ctx.send(f"/ban {user} {reason}")
            await ctx.send(f"Au revoir {user} HeyGuys")

    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user):
        if ctx.author.is_mod:
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
            if name[0] == '@':
                name = name[1:]
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

    @commands.command(name="cursed")
    async def cursed(self, ctx: commands.Context):
        await ctx.send("C'est non")

    @commands.command(name="boubou")
    async def boubou(self, ctx: commands.Context):
        await ctx.send(f'Désolé @Lickers__!')

    @commands.command(name="fx")
    async def fx(self, ctx: commands.Context):
        await ctx.send('Kel bo fx')

    @commands.command(name="lurk")
    async def lurk(self, ctx: commands.Context):
        await ctx.send(f'{ctx.author.name} devient un lurkeur fou!')

    @commands.command(name='shoutout', aliases=['so'])
    async def shoutout(self, ctx: commands.Context, name):
        await ctx.send('yapadeso')
        if ctx.author.is_mod:
            if name[0] == '@':
                name = name[1:]
            await asyncio.sleep(5)
            game = await self.get_game(name)
            await ctx.send(f'Je plaisante haha, allez voir @{name} à www.twitch.tv/{name} pour du gaming de qualitay sur {game}')

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

    @commands.command(name="id")
    async def id(self, ctx: commands.Context):
        await ctx.send(self.mh_id)

    @commands.command(name="setId")
    async def setId(self, ctx: commands.Context, id):
        if ctx.author.is_mod:
            self.mh_id = id
            await ctx.send('id set SeemsGood')

    async def get_game(self, broadcaster: str) -> str:
        """Get the last game played by the specified broadcaster.

        Args:
            broadcaster: Name of the broadcaster whose last game is needed.

        Returns:
            The last game played is returned as string.

        """
        channel_info = await self.bot.fetch_channel(broadcaster)
        return channel_info.game_name


def prepare(bot: commands.Bot):
    bot.add_cog(Misc(bot))
