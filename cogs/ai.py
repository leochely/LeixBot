import logging
import os
from textwrap import wrap

import aiohttp

from twitchio.ext import commands

LLM_API_URL = os.environ.get('LLM_API_URL')

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
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
        logging.debug(self.chat_history[user])
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{LLM_API_URL}/api/chat", 
                json={
                    "messages": self.chat_history[user],
                    "model": "leixbot",
                    "stream":False,
                    "options": {
                        "use_mlock":True,
                        "num_predict": 120
                        }
                    }) as resp:
                data = await resp.json()
                logging.debug(data['message']['content'])
                response = data['message']['content']
                self.chat_history[user].append(
                    {
                        "role": "assistant",
                        "content":response
                    },
                )
                response_chunked = wrap(response, 500)
                for chunk in response_chunked:
                    await ctx.send(chunk)

    @commands.command(name="reset")
    async def reset(self, ctx: commands.Context):
        self.chat_history[ctx.author.name] = []
        ctx.send("J'ai effacé notre conversation. Nous pouvons repartir de zéro! :)")


def prepare(bot: commands.Bot):
    bot.add_cog(AI(bot))
