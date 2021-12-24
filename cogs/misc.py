import asyncio
import datetime
import logging
import os

from twitchio import User
from twitchio.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mh_id = {
            x: "id not set!" for x in os.environ['INITIAL_CHANNELS'].split(' ,')
        }

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

    @commands.command(name="salut", aliases=['slt'])
    async def salut(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Salut @{user.name}!')

    @commands.command(name="bn")
    async def bn(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Bonne nuit @{user.name} <3')

    @commands.command(name="uptime")
    async def uptime_command(self, ctx: commands.bot.Context):
        stream = await self.bot.fetch_streams(
            user_logins=[
                ctx.author.channel.name
            ])

        if len(stream) == 0:
            return await ctx.send("Il n'y a pas de live en cours :(")

        uptime = datetime.datetime.now(
            datetime.timezone.utc) - stream[0].started_at
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
    async def shoutout(self, ctx: commands.Context, broadcaster: User
                       ):
        await ctx.send('yapadeso')
        if 'vip' in ctx.author.badges or ctx.author.is_mod:
            channel_info = await self.bot.fetch_channel(broadcaster.name)
            await asyncio.sleep(5)
            if channel_info.game_name:
                await ctx.send(
                    f'Je plaisante haha, allez voir @{broadcaster.name} à www.twitch.tv/{broadcaster.name} pour du gaming de qualitay sur {channel_info.game_name}'
                )
            else:
                await ctx.send(
                    f"Je plaisante haha, @{broadcaster.name} ne stream pas mais c'est quelqu'un de super cool SeemsGood"
                )

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
        await ctx.send(self.mh_id[ctx.author.channel])

    @commands.command(name="setId")
    async def setId(self, ctx: commands.Context, id):
        print(self.mh_id)
        if ctx.author.is_mod:
            self.mh_id[ctx.author.channel] = id
            await ctx.send('id set SeemsGood')


def prepare(bot: commands.Bot):
    bot.add_cog(Misc(bot))
