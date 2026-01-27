import logging

import twitchio
from twitchio.ext import commands

from custom_commands import is_ads_warning

LOGGER: logging.Logger = logging.getLogger("Components.Subscriptions")

class Subscriptions(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot

    @commands.Component.listener()
    async def event_follow(self, message: twitchio.ChannelFollow) -> None:
        channel = message.broadcaster.name
        follower = message.user.display_name
        LOGGER.info(f"New follower {follower} on channel {channel}")
        await message.broadcaster.send_message(
            sender=self.bot.bot_id,
            message=f"Merci pour le follow {follower}! PogChamp",
        )

    @commands.Component.listener()  
    async def event_subscription(self, message: twitchio.ChannelSubscribe) -> None:
        channel = message.broadcaster.name
        user = message.user.name
        LOGGER.debug(f"New subscription on channel {channel} by user {user} with plan {message.tier/1000}")
        await message.broadcaster.send_message(
            sender=self.bot.bot_id,
            message=f"{user} rejoint la legion au tier {message.tier/1000}! PogChamp",
        )

    @commands.Component.listener()
    async def event_subscription_message(self, message: twitchio.ChannelSubscriptionMessage) -> None:
        channel = message.broadcaster.name
        user = message.user.display_name
        LOGGER.debug(f"New subscription message on channel {channel} by user {user} with tier {message.tier/1000} and message {message.text}")
        await message.broadcaster.send_message(
            sender=self.bot.bot_id,
            message=f"{user} est dans la legion depuis {message.cumulative_months}! PogChamp",
        )

    @commands.Component.listener()
    async def event_stream_online(self, message: twitchio.StreamOnline) -> None:
        LOGGER.info(f"{message.broadcaster.name} is live!")
        await message.respond(f"Coucou {message.broadcaster.display_name}, votre fidele LeixBot est pret a vous servir pour votre stream! PogChamp")

    @commands.Component.listener()
    async def event_stream_offline(self, message: twitchio.StreamOffline) -> None:
        LOGGER.info(f"{message.broadcaster.name} is offline now.")
        await message.respond(f"Au revoir {message.broadcaster.display_name}! A la prochaine fois! DinoDance")

    @commands.Component.listener()
    async def event_raid(self, message: twitchio.ChannelRaid) -> None:
        LOGGER.info(f"{message.from_broadcaster} is raiding {message.to_broadcaster} with {message.viewer_count} viewers!")
        await message.to_broadcaster.send_message(
            sender=self.bot.bot_id,
            message=f"Il faut se defendre SwiftRage Nous sommes raid par {message.from_broadcaster.display_name} avec ses {message.viewer_count} margoulins!",
        )

    @commands.Component.listener()
    async def event_ad_break(self, message: twitchio.ChannelAdBreakBegin) -> None:
        LOGGER.info(f"Ad break started on {message.broadcaster.name} for {message.duration} seconds!")
        if await is_ads_warning(message.broadcaster.id):
            await message.broadcaster.send_message(
                sender=self.bot.bot_id,
                message=f"Pub en cours mais ne vous inquietez pas, LeixBot ne prend pas de pause MrDestructoid",
            )

    @commands.Component.listener()
    async def event_bits_used(self, message: twitchio.ChannelBitsUse) -> None:
        LOGGER.info(f"{message.user.name} used {message.bits} bits on {message.broadcaster.display_name}!")
        await message.broadcaster.send_message(
            sender=self.bot.bot_id,
            message=f"Merci {message.user.display_name} pour les {message.bits} bits! Tu connais TwitchRPG? 👀",
        )

    @commands.Component.listener()
    async def event_hype_train_begin(self, message: twitchio.HypeTrainBegin) -> None:
        LOGGER.info(f"Hype Train started on {message.broadcaster.name}!")
        await message.broadcaster.send_message(
            sender=self.bot.bot_id,
            message=f"Un Train de la Hype commence! Allons-y tout le monde! PewPewPew",
        )

async def setup(bot: commands.AutoBot):
    await bot.add_component(Subscriptions(bot))
