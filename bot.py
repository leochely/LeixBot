import asyncio
import logging
import asqlite
import os
from pathlib import Path
from typing import TYPE_CHECKING

import twitchio
from twitchio.ext import commands
from twitchio import eventsub, web

from utils import auto_so, random_bot_reply, random_reply

if TYPE_CHECKING:
    import sqlite3

LOGGER: logging.Logger = logging.getLogger("Bot")

CLIENT_ID: str = os.environ['CLIENT_ID'] # The CLIENT ID from the Twitch Dev Console
CLIENT_SECRET: str = os.environ['CLIENT_SECRET'] # The CLIENT SECRET from the Twitch Dev Console
BOT_ID = "734769203"  # The Account ID of the bot user...
OWNER_ID = "109173981"  # Your personal User ID..


class LeixBot(commands.AutoBot):
    def __init__(self, token_database: asqlite.Pool, subs: list[twitchio.eventsub.SubscriptionPayload], *args, **kwargs) -> None:
        self.token_database = token_database
        self.connected_channels = []
        self.vip_so = {}
        self._components_names: t.Dict[str] = [
            p.stem for p in Path(".").glob("./components/*.py")
        ]
        
        LOGGER.info(f"Found components: {self._components_names}")
        super().__init__(*args, **kwargs, 
                         subscriptions=subs,
                         adapter = web.AiohttpAdapter(host="0.0.0.0", domain="leixbot.onrender.com")
                        )

    async def setup_hook(self) -> None:
        async with self.token_database.acquire() as connection:
            users = await connection.fetchall(
                """SELECT user_id FROM tokens"""
            )
        for (user_id,) in users:
            self.connected_channels.append(user_id)
            self.vip_so[user_id] = []

        LOGGER.info(f"Managing SOs for {self.vip_so} VIP channels.")

        # Add our components
        await self.add_component(MyComponent(self))
        for component in self._components_names:
            LOGGER.info(f"Loading `{component}` component.")
            await self.load_module(f"components.{component}")

    async def event_oauth_authorized(self, payload: twitchio.authentication.UserTokenPayload) -> None:
        await self.add_token(payload.access_token, payload.refresh_token)

        if not payload.user_id:
            return

        # A list of subscriptions we would like to make to the newly authorized channel...
        subs: list[eventsub.SubscriptionPayload] = [
            eventsub.ChatMessageSubscription(broadcaster_user_id=payload.user_id, user_id=self.bot_id),
            # TODO: Add more subscriptions here...
        ]

        resp: twitchio.MultiSubscribePayload = await self.multi_subscribe(subs)
        if resp.errors:
            LOGGER.warning("Failed to subscribe to: %r, for user: %s", resp.errors, payload.user_id)

    async def add_token(self, token: str, refresh: str) -> twitchio.authentication.ValidateTokenPayload:
        # Make sure to call super() as it will add the tokens interally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(token, refresh)

        # Store our tokens in a simple SQLite Database when they are authorized...
        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def event_ready(self) -> None:
        LOGGER.info("Successfully logged in as: %s", self.bot_id)


    async def event_message(self, message: twitchio.ChatMessage) -> None:
        # Ignore own messages
        if message.chatter.id == self.bot_id:
            return

        try:
            if "@leixbot" in message.text.lower():
                await random_reply(self, message)
            # elif message.chatter.name.lower() in self.bot_to_reply and custom_commands.is_bot_reply(ctx.author.channel.name):
            #     await random_bot_reply(message)
            # else:
            #     await auto_so(self, message, self.vip_so[message.broadcaster.id])
        except Exception as e:
            LOGGER.error(f"Error processing message {message}: {e}")

        await self.process_commands(message)
class MyComponent(commands.Component):
    def __init__(self, bot: LeixBot):
        # Passing args is not required...
        # We pass bot here as an example...
        self.bot = bot

    # We use a listener in our Component to display the messages received.
    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")

    @commands.command(aliases=["hello", "howdy", "hey"])
    async def hi(self, ctx: commands.Context) -> None:
        """Simple command that says hello!

        !hi, !hello, !howdy, !hey
        """
        await ctx.reply(f"Coucou {ctx.chatter.mention}! Ca faisait si longtemps!")

    @commands.group(invoke_fallback=True)
    async def socials(self, ctx: commands.Context) -> None:
        """Group command for our social links.

        !socials
        """
        await ctx.send("discord.gg/..., youtube.com/..., twitch.tv/...")

    @socials.command(name="discord")
    async def socials_discord(self, ctx: commands.Context) -> None:
        """Sub command of socials that sends only our discord invite.

        !socials discord
        """
        await ctx.send("discord.gg/...")

    @commands.command(aliases=["repeat"])
    @commands.is_moderator()
    async def say(self, ctx: commands.Context, *, content: str) -> None:
        """Moderator only command which repeats back what you say.

        !say hello world, !repeat I am cool LUL
        """
        await ctx.send(content)

    @commands.Component.listener()
    async def event_stream_online(self, payload: twitchio.StreamOnline) -> None:
        # Event dispatched when a user goes live from the subscription we made above...
        await payload.broadcaster.send_message(
            sender=self.bot.bot_id,
            message=f"Hi... {payload.broadcaster}! You are live!",
        )


async def setup_database(db: asqlite.Pool) -> tuple[list[tuple[str, str]], list[eventsub.SubscriptionPayload]]:
    # Create our token table, if it doesn't exist..
    # You should add the created files to .gitignore or potentially store them somewhere safer
    # This is just for example purposes...

    query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
    async with db.acquire() as connection:
        await connection.execute(query)

        # Fetch any existing tokens...
        rows: list[sqlite3.Row] = await connection.fetchall("""SELECT * from tokens""")

        tokens: list[tuple[str, str]] = []
        subs: list[eventsub.SubscriptionPayload] = []

        for row in rows:
            tokens.append((row["token"], row["refresh"]))

            if row["user_id"] == BOT_ID:
                continue

            subs.extend([eventsub.ChatMessageSubscription(broadcaster_user_id=row["user_id"], user_id=BOT_ID)])

    return tokens, subs


def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    subs = [
        eventsub.ChatMessageSubscription(broadcaster_user_id=OWNER_ID, user_id=BOT_ID),
        eventsub.ChatMessageSubscription(broadcaster_user_id=BOT_ID, user_id=BOT_ID),
    ]

    async def runner() -> None:
        async with asqlite.create_pool("tokens.db") as tdb:
            tokens, subs = await setup_database(tdb)

            async with LeixBot(subs=subs, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, bot_id=BOT_ID, prefix='!', token_database=tdb) as bot:
                for pair in tokens:
                    await bot.add_token(*pair)

                await bot.start(load_tokens=False)

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt")


if __name__ == "__main__":
    main()