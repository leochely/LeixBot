import logging
import re

from twitchio.ext import commands
from websockets import connect

import custom_commands
from utils import check_cooldown, get_emote_list


KAPPAGEN_DEFAULT_VALUE = 500

# Websocket connection parameters
WS_URL = "ws://57.128.22.87/externalwebsocket"
headers = {
    "api-key": "myKey"
}
protocols = ["external"]



class Visuals(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx: commands.Context):
        return ctx.author.is_mod or 'vip' in ctx.author.badges

    async def cog_command_error(self, ctx: commands.Context, error):
        """
        Not functional yet. Waiting for a twitchio fix.
        """
        logging.info(
            'User not moderator'
        )
        await ctx.send(f"@{ctx.author.name} tu n'es pas modérateur ou VIP!")

    ### COUNTERS ###
    @commands.command(name="rip", aliases=['counter'])
    async def rip(self, ctx: commands.Context):
        """Incrémente le compteur et lance une animation."""
        channel = ctx.author.channel.name

        value = custom_commands.get_counter(channel)
        value += 1
        custom_commands.set_counter(channel, value)
        
        data = {'command' : 'PLAY',
                'page' : 'RIP',
                'content': {
                    'value': value
                },
                'channel': channel}
        
        async with connect(WS_URL, extra_headers=headers, subprotocols=protocols) as session:
            await session.send(str({'command': 'REGISTER', 'page': 'TWITCH_EVENT'}))
            await session.send(str(data))
            await session.close()

    @commands.command(name="resetRip", aliases=['counterReset'])
    async def reset_rip(self, ctx: commands.Context):
        """Réinitialise le compteur et lance une animation.
        Ex: !setRip 123
        """
        channel = ctx.author.channel.name
        
        custom_commands.set_counter(channel, 0)

        data = {'command' : 'PLAY',
        'page' : 'RIP',
        'content': {
            'value': 0
        },
        'channel': channel}
        
        async with connect(WS_URL, extra_headers=headers, subprotocols=protocols) as session:
            await session.send(str({'command': 'REGISTER', 'page': 'TWITCH_EVENT'}))
            await session.send(str(data))
            await session.close()

    @commands.command(name="setRip", aliases=['setCounter'])
    async def set_rip(self, ctx: commands.Context, value: int):
        """Règle le compteur à la valeur donnée et lance une animation."""

        channel = ctx.author.channel.name
        custom_commands.set_counter(channel, int(value))

        data = {'command' : 'PLAY',
                'page' : 'RIP',
                'content': {
                    'value': int(value)
                },
                'channel': channel}
        
        async with connect(WS_URL, extra_headers=headers, subprotocols=protocols) as session:
            await session.send(str({'command': 'REGISTER', 'page': 'TWITCH_EVENT'}))
            await session.send(str(data))
            await session.close()

    ### KAPPAGEN ###
    @commands.command(name="kappagen")
    async def kappagen(self, ctx: commands.Context, value=None):
        """Lance l'animation de kappagen avec le nombre d'emotes (max 999) et
        les emotes spécifiées.
        Ex: !kappagen 123 emote1 emote2 ...
        """
        user = await ctx.author.channel.user()

        # Exits if the user is on cooldown
        if not (check_cooldown(user.name, ctx.author.name)):
            return
        
        # Sets default value if not passed or invalid
        if not value or not value.isnumeric():
            value = KAPPAGEN_DEFAULT_VALUE

        # Parsing emote tags to generate URLs
        emotes_raw = ctx.message.tags['emotes']
        emotes_urls = None
        if len(emotes_raw) > 0:
            emotes_urls = []
            emotes = re.findall('(.*?):', emotes_raw)
            for emote in emotes:
                emote_clean = re.sub(".*/", "", emote)
                emotes_urls.append(
                    "https://static-cdn.jtvnw.net/emoticons/v2/" + emote_clean + "/default/light/3.0"
                )
        else:
            emotes_urls = await get_emote_list(user)

        data = {'command' : 'PLAY',
                'page' : 'KAPPAGEN',
                'content': {
                    'emotes': emotes_urls,
                    'value': value
                },
                'channel': user.name}
        
        async with connect(WS_URL, extra_headers=headers, subprotocols=protocols) as session:
            await session.send(str({'command': 'REGISTER', 'page': 'TWITCH_EVENT'}))
            await session.send(str(data))
            await session.close()

    @commands.command(name="kappagenCooldown")
    async def kappagen_cooldown(self, ctx: commands.Context, value: int):
        """Règle le cooldown du kappagen (en secondes) pour les utilisateurs non modérateurs.
        Ex: !kappagenCooldown 123
        """
        if not ctx.author.is_mod:
            return

        if value > 0:
            logging.info('test')
            custom_commands.set_kappagen_cooldown(
                ctx.author.channel.name, value)


def prepare(bot: commands.Bot):
    bot.add_cog(Visuals(bot))
