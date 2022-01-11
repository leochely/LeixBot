import logging
import os

from twitchio import Channel, Game
from twitchio.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.is_mod

    async def cog_command_error(self, ctx, error):
        """
        Not functional yet. Waiting for a twitchio fix.
        """
        logging.info(
            'Error in {0.command.qualified_name}: {1}'.format(ctx, error)
        )

    @commands.command(name="ban")
    async def ban(self, ctx: commands.Context, user, reason="rise of the machines"):
        await ctx.send(f"/ban {user} {reason}")
        await ctx.send(f"Au revoir {user} HeyGuys")

    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user):
        await ctx.send(f"/unban {user}")
        await ctx.send(f"Bon retour parmi nous {user} HeyGuys !")

    @commands.command(name="title")
    async def title(self, ctx: commands.Context, *title):
        u: List["User"] = await self.bot.fetch_users(names=[ctx.author.channel.name])
        channel: Channel = u[0]
        await channel.modify_stream(os.environ['CHANNEL_ACCESS_TOKEN'], title=' '.join(title))
        await ctx.send('Title updated SeemsGood')

    @commands.command(name="game")
    async def game(self, ctx: commands.Context, *game_name):
        u: List["User"] = await self.bot.fetch_users(names=[ctx.author.channel.name])
        channel: Channel = u[0]
        g: List["Games"] = await self.bot.fetch_games(names=[' '.join(game_name)])
        game: Game = g[0]

        await channel.modify_stream(os.environ['CHANNEL_ACCESS_TOKEN'], game_id=game.id)
        await ctx.send('Game updated SeemsGood')


def prepare(bot: commands.Bot):
    bot.add_cog(Mod(bot))