import logging
import os

from twitchio import Game, User
from twitchio.ext import commands

LOGGER: logging.Logger = logging.getLogger("Components.Mod")
class Mod(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        """
        Not functional yet. Waiting for a twitchio fix.
        """
        await ctx.reply('Wsh t pas modo')

        LOGGER.info(
            'User not moderator'
        )

    @commands.command(name="ban")
    async def ban(self, ctx: commands.Context, user: User = None, *reason):
        """Banni un utilisateur avec possibilité d'ajouter une raison. Requiert
        privilège modérateur.
        Ex: !ban leix34 motif du ban
        """
        LOGGER.info(f'User {user.name} has been banned')
        if not reason:
            reason = 'Rise of the machines'
        else:
            reason = ' '.join(reason)
        await ctx.send(f"/ban {user.name} {reason}")
        await ctx.send(f"Au revoir {user.name} HeyGuys")

    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user: User = None):
        """Retire le banissement d'un utilisateur. Requiert
        privilège modérateur.
        Ex: !unban leix34
        """
        LOGGER.info(f'User {user.name} has been unbanned')
        await ctx.send(f"/unban {user.name}")
        await ctx.send(f"Bon retour parmi nous {user.name} HeyGuys !")


async def setup(bot: commands.AutoBot):
    await bot.add_component(Mod(bot))
