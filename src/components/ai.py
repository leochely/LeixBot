import logging
import os
from textwrap import wrap

import aiohttp

from twitchio.ext import commands

LOGGER: logging.Logger = logging.getLogger("AI")

LLM_API_URL = os.environ.get('LLM_API_URL')

class AI(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot
        self.chat_history = {}

    @commands.command(name="chat")
    async def chat(self, ctx: commands.Context, *prompt):
        """Chat avec l'IA de LeixBot. Ex: !chat Wsh t ki?"""
        user = ctx.author.name
        prompt = ' '.join(prompt)
        self.chat_history.setdefault(user,[]).append(
            {
            "role": "user",
            "content":prompt
            },
        )
        LOGGER.debug(self.chat_history[user])
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{LLM_API_URL}/api/chat", 
                json={
                    "messages": self.chat_history[user],
                    "model": "leixbot",
                    "stream":False,
                    "options": {
                        "use_mlock":True
                        }
                    }) as resp:
                data = await resp.json()
                LOGGER.debug(data['message']['content'])
                response = data['message']['content']
                self.chat_history[user].append(
                    {
                        "role": "assistant",
                        "content":response
                    },
                )
                response_chunked = wrap(response, 500)
                for chunk in response_chunked:
                    await ctx.reply(chunk)

    @commands.command(name="reset")
    async def reset(self, ctx: commands.Context):
        """Efface l'historique de conversation avec l'IA. Ex: !reset"""
        self.chat_history[ctx.author.name] = []
        await ctx.reply("J'ai effacé notre conversation. Nous pouvons repartir de zéro! :)")


async def setup(bot: commands.AutoBot):
    await bot.add_component(AI(bot))
