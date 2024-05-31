import discord
from discord.ext import commands
from PyQt5.QtCore import pyqtSignal, QObject
import json
import os


class RewardSystem(commands.Cog):
    # signal to notify the GUI that user data has been modified
    # user_modified = pyqtSignal()

    def __init__(self, bot):
        self.bot = bot
        self.user_fetcher = bot.get_cog('UserFetcher')

    @commands.Cog.listener()
    async def on_message(self, message):
        # if message.author.bot:
        # return

        user_id = str(message.author.id)

        behaviour_points = len(message.content) * 0.1
        self.modify_user(user_id, {
            'behaviour_points': behaviour_points,
            'reward_points': behaviour_points * 0.1
        })

    @commands.command(name="points", description="Check user points")
    async def points(self, ctx):
        user_data = self.user_fetcher.get_user_data(str(ctx.author.id))
        behaviour_points = user_data.get('behaviour_points', 0)
        reward_points = user_data.get('reward_points', 0)
        await ctx.send(
            f'{ctx.author.mention} has {behaviour_points:.2f} behaviour points and {reward_points:.2f} reward points.')

    @commands.command(name="punish", description="Punish a user")
    @commands.has_permissions(administrator=True)
    async def punish(self, ctx, user: discord.Member, points: int):
        user_id = str(user.id)
        user_data = self.user_fetcher.get_user_data(user_id)
        if user_data:
            user_data['behaviour_points'] = user_data['behaviour_points'] - points
            self.user_fetcher.set_user_data(user_id, user_data)
        else:
            print(f"User {user_id} not found.")
        await ctx.send(f'{user.mention} has been punished with {points} behaviour points.')

    def modify_user(self, user_id, data):
        user_data = self.user_fetcher.get_user_data(user_id)
        user_data['behaviour_points'] = max(min(user_data['behaviour_points'] + data.get('behaviour_points', 0), 1000),
                                            -1000)
        user_data['reward_points'] = max(min(user_data['reward_points'] + data.get('reward_points', 0), 1000), -1000)
        self.user_fetcher.set_user_data(user_id, user_data)
        # self.user_modified.emit()


async def setup(bot):
    await bot.add_cog(RewardSystem(bot))
