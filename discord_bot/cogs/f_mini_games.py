import discord
from discord.ext import commands
import asyncio
import random


class MiniGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quiz(self, ctx):
        question = "What is the capital of France?"
        options = ["A) London", "B) Paris", "C) Berlin", "D) Madrid"]
        answer = "B"

        await ctx.send(f'{question}\n{"\n".join(options)}')

        def check(m):
            return m.author == ctx.author and m.content.upper() in ["A", "B", "C", "D"]

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(f'Time is up! The correct answer was {answer}.')
            return

        if msg.content.upper() == answer:
            await ctx.send('Correct!')
        else:
            await ctx.send(f'Wrong! The correct answer was {answer}.')


async def setup(bot):
    await bot.add_cog(MiniGames(bot))
