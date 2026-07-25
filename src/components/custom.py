from encodings.aliases import aliases
import logging

from twitchio import User
from twitchio.ext import commands

import custom_commands

LOGGER: logging.Logger = logging.getLogger("Components.Custom")

class CustomCommand(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.is_mod

    @commands.is_moderator()
    @commands.command(name="cmdadd", aliases=["cmd_add"])
    async def cmdadd(self, ctx: commands.Context, command, *text):
        """Ajoute une commande a la base de données.
        Ex: !cmdadd !test ma commande
        """
        channel_id = ctx.broadcaster.id
        text = ' '.join(text)

        await custom_commands.add_command(command, channel_id, text)

        await ctx.send(f"Commande {command} ajoutée avec succes SeemsGood")

    @commands.is_moderator()
    @commands.command(name="cmdedit", aliases=["cmd_edit"])
    async def cmdedit(self, ctx: commands.Context, command, *text):
        """Edite une commande presente dans la base de données.
        Ex: !cmdedit !test mon nouveau texte de commande
        """
        channel_id = ctx.broadcaster.id
        text = ' '.join(text)

        await custom_commands.edit_command(command, channel_id, text)

        await ctx.send(f"Commande {command} éditée avec succes SeemsGood")

    @commands.is_moderator()
    @commands.command(name="cmdremove", aliases=["cmd_remove"])
    async def cmdremove(self, ctx: commands.Context, command):
        """
        Retire une commande de la base de données.
        Ex: !cmdremove !test
        """
        channel_id = ctx.broadcaster.id

        await custom_commands.remove_command(command, channel_id)

        await ctx.send(f"Commande {command} retirée avec succes SeemsGood")
    
    @commands.is_moderator()
    @commands.command(name="disableautosovip", aliases=["disable_auto_so_vip"])
    async def disableautosovip(self, ctx: commands.Context):
        """Désactive le shoutout automatique pour les VIP et modérateurs"""
        await custom_commands.update_vip_so(ctx.broadcaster.id, False)
        await ctx.send('Le so automatique a été désactivé SeemsGood')

    @commands.is_moderator()
    @commands.command(name="enableautosovip", aliases=["enable_auto_so_vip"])
    async def enableautosovip(self, ctx: commands.Context):
        """Active le shoutout automatique pour les VIP et modérateurs"""
        await custom_commands.update_vip_so(ctx.broadcaster.id, True)
        await ctx.send('Le so automatique a été activé SeemsGood')

    @commands.is_moderator()
    @commands.command(name="disablebotreplies", aliases=["disable_bot_responses"])
    async def disablebotreplies(self, ctx: commands.Context):
        """Désactive les réponses automatiques aux bots"""
        await custom_commands.update_bot_replies(ctx.broadcaster.id, False)
        await ctx.send('Les réponses automatiques aux bots ont été désactivées SeemsGood')

    @commands.is_moderator()
    @commands.command(name="enablebotreplies", aliases=["enablebotresponses"])
    async def enablebotreplies(self, ctx: commands.Context):
        """Active les réponses automatiques aux bots"""
        await custom_commands.update_bot_replies(ctx.broadcaster.id, True)
        await ctx.send('Les réponses automatiques aux bots ont été activées SeemsGood')

    @commands.command(name="enableadswarning", aliases=["enable_ads_warning"])
    async def enableadswarning(self, ctx: commands.Context):
        """Active l'avertissement de pub avant les pauses publicitaires"""
        await custom_commands.update_ads_warning(ctx.broadcaster.id, True)
        await ctx.send("L'avertissement de pub avant les pauses publicitaires a été activé SeemsGood")

    @commands.command(name="disableadswarning", aliases=["disable_ads_warning"])
    async def disableadswarning(self, ctx: commands.Context):
        """Désactive l'avertissement de pub avant les pauses publicitaires"""
        await custom_commands.update_ads_warning(ctx.broadcaster.id, False)
        await ctx.send("L'avertissement de pub avant les pauses publicitaires a été désactivé SeemsGood")



async def setup(bot: commands.AutoBot):
    await bot.add_component(CustomCommand(bot))
