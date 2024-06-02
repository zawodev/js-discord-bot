import discord
from discord.ext import commands
import json

from utils.saving_loading_json import load_setting_json, save_setting_json

class UserFetcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.guilds[0]
        self.user_data = load_setting_json('user_data')

    def save_user_data(self):
        save_setting_json('user_data', self.user_data)

    async def fetch_users(self):
        guild_users = {}
        for member in self.guild.members:
            user_id = str(member.id)
            guild_users[user_id] = self.get_user_data(user_id)

        return guild_users

    def _create_empty_user(self, user_id):
        member = self.guild.get_member(int(user_id))
        if member:
            new_user_data = {
                'behaviour_points': 0,
                'reward_points': 0,
                'messages_count': 0,
                'name': str(member),
                'avatar_url': str(member.avatar.url if member.avatar else "")
            }
            return new_user_data
        print(f"Error: user {user_id} not found.")
        return None

    def get_user_data(self, user_id):
        return self.user_data.get(str(user_id), self._create_empty_user(user_id))

    def set_user_data(self, user_id, data):
        self.user_data[user_id] = data
        self.save_user_data()

async def setup(bot):
    await bot.add_cog(UserFetcher(bot))
