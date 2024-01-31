import logging
import os

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
        logging.info(self.chat_history[user])
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{LLM_API_URL}/api/chat", 
                json={
                    "messages": self.chat_history[user],
                    "model": "leixbot",
                    "stream":False,
                    "num_ctx": 200,
                    "use_mlock":True}) as resp:
                data = await resp.json()
                logging.info(data['message']['content'])
                response = data['message']['content']
                await ctx.send(response)
                self.chat_history[user].append(
                    {
                    "role": "assistant",
                    "content":response
                    },
                )


def prepare(bot: commands.Bot):
    bot.add_cog(AI(bot))
