import asyncio
from datetime import datetime, timezone
import secrets
import logging

import wikipediaapi
import humanize

from twitchio import User
from twitchio.ext import commands
from howlongtobeatpy import HowLongToBeat

# Sets humanize to French language
humanize.i18n.activate("fr_FR")
wiki = wikipediaapi.Wikipedia('fr')


LOGGER: logging.Logger = logging.getLogger("Components.Misc")

class Misc(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot
        self.game_id = {}

    @commands.command(name="leixban")
    async def leixban(self, ctx: commands.Context, user):
        """ 'Banni' un utilisateur... pour de faux.
        Ex: !leixban Leix34
        """
        await ctx.send(f"Non t'abuses {ctx.author.name}, on va pas ban {user} quand meme BibleThump")

    @commands.command(name="salut", aliases=['slt'])
    async def salut(self, ctx: commands.Context, *user: User):
        """Transmet vos salutations a un utilisateur. Ex: !slt leix34"""
        if not user:
            user = ctx.author
            await ctx.send(f'Mes salutations les plus distinguées @{user.display_name}! <3')
        elif len(user) == 1:
            await ctx.send(f'Mes salutations les plus distinguées @{user[0].display_name} <3')
        else:
            names = " et ".join(", ".join([x.display_name for x in user]).rsplit(', ', 1))
            await ctx.send(f'Mes salutations les plus distinguées {names} <3')

    @commands.command(name="bn")
    async def bn(self, ctx: commands.Context, *user: User):
        """Souhaite bonne nuit a un utilisateur. Ex: !bn leix34"""
        if not user:
            user = ctx.author
            await ctx.send(f'Fais de beaux rêves @{user.display_name} <3')
        elif len(user) == 1:
            await ctx.send(f'Fais de beaux rêves @{user[0].display_name} <3')
        else:
            names = " et ".join(", ".join([x.display_name for x in user]).rsplit(', ', 1))
            await ctx.send(f'Faites de beaux rêves {names} <3')

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.Context):
        """Donne le temps du live actuel. Ex: !uptime"""
        stream = await self.bot.fetch_streams(
            user_logins=[
                ctx.channel.name
            ])

        if len(stream) == 0:
            return await ctx.send("Il n'y a pas de live en cours :(")

        uptime = datetime.now(
            timezone.utc) - stream[0].started_at
        await ctx.send(f"Ton streamer préféré est en live depuis {humanize.precisedelta(uptime, minimum_unit='seconds')}")

    @commands.command(name="dblade")
    async def dblade(self, ctx: commands.Context):
        """Dédicace une destroyer blade a l'utilisateur. Ex: !dblade"""
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
        """Indique que vous devenez un lurkeur"""
        await ctx.send(f'{ctx.author.name} devient un lurkeur fou!')

    @commands.command(name='shoutout', aliases=['so'])
    async def shoutout(self, ctx: commands.Context, broadcaster: User):
        """Shoutout l'utilisateur choisi. Ex: !so leix34"""
        await ctx.send('yapadeso')
        if ctx.author.vip or ctx.author.moderator:
            channel_info = await self.bot.fetch_channel(broadcaster.id)
            await asyncio.sleep(5)
            if channel_info.game_name:
                await ctx.send(
                    f'Je plaisante haha, allez voir @{broadcaster.display_name} sur www.twitch.tv/{broadcaster.name} pour du gaming de qualitay sur {channel_info.game_name}'
                )
            else:
                await ctx.send(
                    f"Je plaisante haha, @{broadcaster.display_name} ne stream pas mais c'est quelqu'un de super cool SeemsGood"
                )

    @commands.command(name="porte")
    async def porte(self, ctx: commands.Context):
        await ctx.send("Vision d'artiste")

    @commands.command(name="den")
    async def den(self, ctx: commands.Context):
        await ctx.send('https://discord.gg/PEfEVWacgP')

    @commands.command(name="ref")
    async def ref(self, ctx: commands.Context):
        await ctx.send('glaref SwiftRage')

    @commands.command(name="cam")
    async def cam(self, ctx: commands.Context):
        await ctx.send('MET LA CAM')

    @commands.command(name="wikipedia", aliases=['wiki'])
    async def wikipedia(self, ctx: commands.Context, *query):
        """Renvoie la definition wikipedia d'un mot.
        Ex: !wikipedia Kojima
        """
        query = '_'.join(query)
        page = wiki.page(query)
        LOGGER.debug(page.summary.splitlines()[0])
        if page.exists():
            if len(page.summary.splitlines()[0]) > 450:
                await ctx.send(f'Il y a tant a dire! La page pour cette recherche: {page.fullurl }')
            else:
                await ctx.send('. '.join(page.summary.splitlines()[0][:450].split(".")[:-1]) + '. ' + page.fullurl)
        else:
            await ctx.send(f"Je n'ai rien trouvé pour cette recherche :(")

    @commands.command(name="pileouface", aliases=['pile', 'face', 'coinflip'])
    async def pileouface(self, ctx: commands.Context, *query):
        """Fait un pile ou face.
        Ex: !pileouface
        """
        flip = secrets.choice(['pile', 'face'])
        await ctx.send(f'''C'est {flip}!''')

    @commands.command(name='howlong', aliases=['hl2b'])
    async def howlong(self, ctx: commands.Context, *game):
        """Renvoie la durée moyenne d'un jeu sur howlongtobeat.com
        Ex: !howlong The Witcher 3
        """
        game = ' '.join(game)
        results = await HowLongToBeat().async_search(game, similarity_case_sensitive=False)
        LOGGER.debug(results)
        if results is not None and len(results) > 0:
            game_entry = max(results, key=lambda element: element.similarity)
            LOGGER.debug(game_entry)
            main_story = game_entry.main_story
            extra = game_entry.main_extra
            completionist = game_entry.completionist
            all_styles = game_entry.all_styles

            await ctx.send(f'{game_entry.game_name} - Main Story: {main_story}h - Main + Extra: {extra}h - Completionist: {completionist}h - All Styles: {all_styles}h')


    @ commands.command(name='id')
    async def id(self, ctx: commands.Context):
        """Renvoie l'id de la session (si existant). Ex: !id"""
        if ctx.broadcaster.id not in self.game_id:
            await ctx.send("Il n'y a pas d'id :(")
        else:
            await ctx.send(self.game_id[ctx.broadcaster.id])

    @commands.is_moderator()
    @ commands.command(name="setId", aliases=['setid'])
    async def setId(self, ctx: commands.Context, *id):
        """Regle l'id de la session. Ex: !id abc 1234"""
        self.game_id[ctx.broadcaster.id] = ' '.join(id)
        await ctx.send('id set SeemsGood')


async def setup(bot: commands.AutoBot):
    await bot.add_component(Misc(bot))
