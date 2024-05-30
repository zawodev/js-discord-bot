import discord
from discord.ext import commands
from discord import app_commands

class RewardSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_points = {}  # This should be stored persistently
        self.tree = bot.tree

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        self.user_points[message.author.id] = self.user_points.get(message.author.id, 0) + 1

    @app_commands.command(name="points", description="Check user points")
    @app_commands.describe(member="Member to check points for")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def points(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        points = self.user_points.get(member.id, 0)
        await ctx.send(f'{member.mention} has {points} points.')

async def setup(bot):
    await bot.add_cog(RewardSystem(bot))
