import logging

from twitchio import Game, User
from twitchio.ext import commands

class NotModeratorError(commands.GuardFailure):
    """Custom error raised when a user is not a moderator."""
    pass


LOGGER: logging.Logger = logging.getLogger("Components.Mod")
class Mod(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot

    @commands.Component.guard()
    def is_moderator(self, ctx: commands.Context) -> bool:
        if not ctx.chatter.moderator:
            raise NotModeratorError

        return True

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

        await ctx.broadcaster.ban_user(user=user, reason=reason)
        await ctx.send(f"Au revoir {user.name} SwiftRage")
        LOGGER.info(f'User {user.name} has been banned')
        

    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user: User = None):
        """Retire le banissement d'un utilisateur. Requiert
        privilège modérateur.
        Ex: !unban leix34
        """
        await ctx.broadcaster.unban_user(moderator=self.bot.user, user_id=user.id)
        await ctx.send(f"Bon retour parmi nous {user.name} HeyGuys !")
        LOGGER.info(f'User {user.name} has been unbanned')

    @commands.command(name="to")
    async def timeout(self, ctx: commands.Context, user: User = None, duration: int = 600, *, reason: str | None = None):
        """Met en timeout un utilisateur pour une durée définie (en secondes)
        avec possibilité d'ajouter une raison. Requiert privilège modérateur.
        Ex: !to leix34 300 motif du timeout
        """
        if not reason:
            reason = 'Rise of the machines'
        else:
            reason = ' '.join(reason)

        await ctx.broadcaster.timeout_user(moderator=self.bot.user, user=user, duration=duration, reason=reason)
        await ctx.send(f"{user.name} a été mis en timeout pour {duration} secondes SwiftRage")
        LOGGER.info(f'User {user.name} has been timed out for {duration} seconds')

    @commands.command(name="setgame")
    async def set_game(self, ctx: commands.Context, *, game_name: str):
        """PAS FONCTIONNEL. Change le jeu affiché sur le stream. Requiert privilège modérateur.
        Ex: !setgame Just Chatting
        """
        LOGGER.info(f'tokens: {self.bot.tokens}')
        game = await self.bot.fetch_game(name=game_name)
        LOGGER.info(f'Fetched game: {game.name} (ID: {game.id})')
        await ctx.broadcaster.modify_channel(game_id=game.id)
        await ctx.send(f"Le jeu du stream a été changé en {game_name} SeemsGood")
        LOGGER.info(f'Stream game changed to {game_name} by {ctx.author.name}')

    @commands.command(name="settitle")
    async def set_title(self, ctx: commands.Context, *, title: str):
        """PAS FONCTIONNEL. Change le titre affiché sur le stream. Requiert privilège modérateur.
        Ex: !settitle New Stream Title
        """ 
        await ctx.broadcaster.modify_channel(title=title)
        await ctx.send(f"Le titre du stream a été changé en {title} SeemsGood")
        LOGGER.info(f'Stream title changed to {title} by {ctx.author.name}')


    async def component_command_error(self, payload: commands.CommandErrorPayload) -> bool | None:
        error = payload.exception
        ctx = payload.context

        if isinstance(error, NotModeratorError):
            await ctx.reply("Cette commande est réservée aux modérateurs!")

            # This explicit False return stops the error from being dispatched anywhere else...
            return False

async def setup(bot: commands.AutoBot):
    await bot.add_component(Mod(bot))
