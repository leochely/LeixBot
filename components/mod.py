import logging
import os

from twitchio import Game, User
from twitchio.ext import commands

LOGGER: logging.Logger = logging.getLogger("Components.Mod")
class Mod(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot

    @commands.is_moderator()
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

        await ctx.broadcaster.ban_user(moderator=self.bot.user, user=user, reason=reason)
        await ctx.send(f"Au revoir {user.name} SwiftRage")
        LOGGER.info(f'User {user.name} has been banned')
        

    @commands.is_moderator()
    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user: User = None):
        """Retire le banissement d'un utilisateur. Requiert
        privilège modérateur.
        Ex: !unban leix34
        """
        await ctx.broadcaster.unban_user(moderator=self.bot.user, user_id=user.id)
        await ctx.send(f"Bon retour parmi nous {user.name} HeyGuys !")
        LOGGER.info(f'User {user.name} has been unbanned')


async def setup(bot: commands.AutoBot):
    await bot.add_component(Mod(bot))
