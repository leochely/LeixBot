import logging
import os

from twitchio import Game, User
from twitchio.ext import commands

LOGGER: logging.Logger = logging.getLogger("Components.Mod")
class Mod(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot

    @commands.command(name="ban")
    async def ban(self, ctx: commands.Context, user: User = None, *, reason: str | None = None):
        """Banni un utilisateur avec possibilité d'ajouter une raison. Requiert
        privilège modérateur.
        Ex: !ban leix34 motif du ban
        """
        if not reason:
            reason = 'Rise of the machines'
        else:
            reason = ' '.join(reason)

        await user.ban_user(moderator=self.bot.user, user=user, reason=reason)
        LOGGER.info(f'User {user.name} has been banned')
        
    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user: User = None):
        """Retire le banissement d'un utilisateur. Requiert
        privilège modérateur.
        Ex: !unban leix34
        """
        await user.unban_user(moderator=self.bot.user, user=user)
        await ctx.send(f"Bon retour parmi nous {user.name} HeyGuys !")
        LOGGER.info(f'User {user.name} has been unbanned')


async def setup(bot: commands.AutoBot):
    await bot.add_component(Mod(bot))
