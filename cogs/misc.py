import asyncio
import datetime
import logging
import os

import wikiquote
import humanize
import random

from twitchio import User
from twitchio.ext import commands

# Sets humanize to French language
humanize.i18n.activate("fr_FR")


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.game_id = {}
        random.seed(datetime.datetime.now())

    @commands.command(name="leixban")
    async def leixban(self, ctx: commands.Context, user):
        await ctx.send(f"Non t'abuses {ctx.author.name}, on va pas ban {user} quand meme BibleThump")

    @commands.command(name="salut", aliases=['slt'])
    async def salut(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Mes salutations les plus distinguées @{user.name}! <3')

    @commands.command(name="bn")
    async def bn(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Fais de beaux rêves @{user.name} <3')

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.bot.Context):
        stream = await self.bot.fetch_streams(
            user_logins=[
                ctx.author.channel.name
            ])

        if len(stream) == 0:
            return await ctx.send("Il n'y a pas de live en cours :(")

        uptime = datetime.datetime.now(
            datetime.timezone.utc) - stream[0].started_at
        await ctx.send(f"Ton streamer préféré est en live depuis {humanize.precisedelta(uptime, minimum_unit='seconds')}")

    @commands.command(name="dblade")
    async def dblade(self, ctx: commands.Context):
        await ctx.send(f'Je te dédicace cette dblade {ctx.author.name}!')

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
    async def shoutout(self, ctx: commands.Context, broadcaster: User):
        await ctx.send('yapadeso')
        if 'vip' in ctx.author.badges or ctx.author.is_mod:
            channel_info = await self.bot.fetch_channel(broadcaster.name)
            await asyncio.sleep(5)
            if channel_info.game_name:
                await ctx.send(
                    f'Je plaisante haha, allez voir @{broadcaster.name} sur www.twitch.tv/{broadcaster.name} pour du gaming de qualitay sur {channel_info.game_name}'
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

    @commands.command(name="citation", aliases=['quote'])
    async def citation(self, ctx: commands.Context, *author):
        if not author:
            author = wikiquote.random_titles(max_titles=1, lang='fr')[0]
        else:
            author = ' '.join(author)
            author = wikiquote.search(author, lang='fr')

        if author:
            quote = random.choice(wikiquote.quotes(author[0], lang='fr'))
            await ctx.send(f'{quote} - {author[0]}')
        else:
            await ctx.send(f"Je n'ai rien trouvé pour cette recherche :(")

    @commands.command()
    async def id(self, ctx: commands.Context):
        if ctx.author.channel.name not in self.game_id:
            await ctx.send("Il n'y a pas d'id :(")
        else:
            await ctx.send(self.game_id[ctx.author.channel.name])

    @commands.command(name="setId")
    async def setId(self, ctx: commands.Context, *id):
        if ctx.author.is_mod:
            self.game_id[ctx.author.channel.name] = ' '.join(id)
            await ctx.send('id set SeemsGood')


def prepare(bot: commands.Bot):
    bot.add_cog(Misc(bot))
