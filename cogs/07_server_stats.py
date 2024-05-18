import discord
from discord.ext import commands
from collections import Counter

class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_counter = Counter()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            self.message_counter[message.author.id] += 1

    @commands.command()
    async def stats(self, ctx):
        most_active = self.message_counter.most_common(1)
        if most_active:
            user_id, count = most_active[0]
            user = self.bot.get_user(user_id)
            await ctx.send(f'The most active user is {user.mention} with {count} messages.')
        else:
            await ctx.send('No messages have been counted yet.')

async def setup(bot):
    await bot.add_cog(Statistics(bot))
