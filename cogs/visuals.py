import socketio
import logging
import re

from twitchio.ext import commands

import custom_commands

sio = socketio.AsyncClient()


@sio.event
def disconnect():
    logging.info('disconnected')


class Visuals(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.is_mod or 'vip' in ctx.author.badges

    async def cog_command_error(self, ctx, error):
        """
        Not functional yet. Waiting for a twitchio fix.
        """
        logging.info(
            'User not moderator'
        )
        await ctx.send(f"@{user.name} tu n'es pas modérateur ou VIP!")

    ### COUNTERS ###
    @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command(name="rip")
    async def rip(self, ctx: commands.Context):
        channel = ctx.author.channel.name
        await sio.connect('http://195.201.111.178:3000', wait_timeout=10)
        value = custom_commands.get_counter(channel)
        logging.info(value)
        value += 1
        custom_commands.set_counter(channel, value)
        data = {
            'channel': channel,
            'params': {
                'value': value,
            }
        }
        await sio.emit('leixbot.rip', data)

    @commands.command(name="reset_rip")
    async def reset_rip(self, ctx: commands.Context):
        channel = ctx.author.channel.name
        await sio.connect('http://195.201.111.178:3000', wait_timeout=10)
        custom_commands.set_counter(channel, 0)
        data = {
            'channel': channel,
            'params': {
                'value': 0,
            }
        }
        await sio.emit('leixbot.rip', data)

    @commands.command(name="set_rip")
    async def set_rip(self, ctx: commands.Context, value):
        channel = ctx.author.channel.name
        await sio.connect('http://195.201.111.178:3000', wait_timeout=10)
        custom_commands.set_counter(channel, int(value))
        data = {
            'channel': channel,
            'params': {
                'value': int(value),
            }
        }
        await sio.emit('leixbot.rip', data)

    ### KAPPAGEN ###
    @commands.cooldown(1, 30, commands.Bucket.user)
    @commands.command(name="kappagen")
    async def kappagen(self, ctx: commands.Context, value=None):
        channel = ctx.author.channel.name
        await sio.connect('http://195.201.111.178:3000', wait_timeout=10)
        if not value or not value.isnumeric():
            value = None

        # Parsing emote tags to generate URLs
        emotes_raw = ctx.message.tags['emotes']
        emotes_urls = None
        if len(emotes_raw) > 0:
            emotes_urls = []
            emotes = re.findall('(.*?):', emotes_raw)
            for emote in emotes:
                emote_clean = re.sub(".*/", "", emote)
                emotes_urls.append(
                    "https://static-cdn.jtvnw.net/emoticons/v2/" + emote_clean + "/default/light/1.0"
                )

        logging.info(value)
        data = {
            'channel': channel,
            'params': {
                'value': value,
                'emotes': emotes_urls,
            }
        }

        await sio.emit('leixbot.kappagen', data)


def prepare(bot: commands.Bot):
    bot.add_cog(Visuals(bot))
