import discord
from discord.ext import commands
from PyQt5.QtCore import pyqtSignal, QObject
import json
import os

from utils.saving_loading_json import load_setting_json, save_setting_json


class RewardSystem(commands.Cog):
    # signal to notify the GUI that user data has been modified
    # user_modified = pyqtSignal()

    def __init__(self, bot):
        self.bot = bot
        self.user_data = load_setting_json('user_data')

    @commands.Cog.listener()
    async def on_message(self, message):
        # if message.author.bot:
        # return

        user_id = str(message.author.id)

        behaviour_points = len(message.content) * 0.1
        self.modify_user(user_id, {
            'is_on_server': True,
            'messages_count': 1,
            'behaviour_points': behaviour_points,
            'reward_points': behaviour_points * 0.1
        })

    @commands.command(name="points", description="Check user points")
    async def points(self, ctx):
        user_data = self.user_data.get(str(ctx.author.id), {})
        behaviour_points = user_data.get('behaviour_points', 0)
        reward_points = user_data.get('reward_points', 0)
        await ctx.send(
            f'{ctx.author.mention} has {behaviour_points:.2f} behaviour points and {reward_points:.2f} reward points.')

    @commands.command(name="punish", description="Punish a user")
    @commands.has_permissions(administrator=True)
    async def punish(self, ctx, user: discord.Member, points: int):
        user_id = str(user.id)
        user_data = self.user_data.get(user_id, {})
        if user_data:
            user_data['behaviour_points'] = user_data['behaviour_points'] - points
            self.user_data[user_id] = user_data
            save_setting_json('user_data', self.user_data)
        else:
            print(f"User {user_id} not found.")
        await ctx.send(f'{user.mention} has been punished with {points} behaviour points.')

    def modify_user(self, user_id, data):
        user_id = str(user_id)
        if user_id not in self.user_data:
            self.user_data[user_id] = data
        else:
            self.user_data[user_id]['behaviour_points'] = max(
                min(self.user_data[user_id].get('behaviour_points', 0) + data.get('behaviour_points', 0), 1000), -1000)
            self.user_data[user_id]['reward_points'] = max(
                min(self.user_data[user_id].get('reward_points', 0) + data.get('reward_points', 0), 1000), -1000)
            self.user_data[user_id]['messages_count'] = self.user_data[user_id].get('messages_count', 0) + data.get(
                'messages_count', 0)
            if 'is_on_server' in data:
                self.user_data[user_id]['is_on_server'] = data['is_on_server']
        save_setting_json('user_data', self.user_data)
        # self.user_modified.emit()


async def setup(bot):
    await bot.add_cog(RewardSystem(bot))
