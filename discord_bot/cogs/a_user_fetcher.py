import discord
from discord.ext import commands
import json

class UserFetcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.guilds[0]
        self.user_data_file = 'user_data.json'
        self.user_data = self.load_user_data()

    def load_user_data(self):
        try:
            with open(self.user_data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print(f"Error: {self.user_data_file} is not a valid JSON file.")
            return {}

    def save_user_data(self):
        with open(self.user_data_file, 'w') as file:
            json.dump(self.user_data, file)

    async def fetch_users(self):
        guild_users = {}
        for member in self.guild.members:
            user_id = str(member.id)
            guild_users[user_id] = self.get_user_data(user_id)

        self.user_data.update(guild_users)
        self.save_user_data()
        return guild_users

    def _create_empty_user(self, user_id):
        member = self.guild.get_member(int(user_id))
        if member:
            new_user_data = {
                'behaviour_points': 0,
                'reward_points': 0,
                'username': str(member),
                'avatar_url': str(member.avatar.url if member.avatar else "")
            }
            return new_user_data
        print(f"Error: user {user_id} not found.")
        return None

    def get_user_data(self, user_id):
        return self.user_data.get(user_id, self._create_empty_user(user_id))

    def set_user_data(self, user_id, data):
        self.user_data[user_id] = data
        self.save_user_data()

async def setup(bot):
    await bot.add_cog(UserFetcher(bot))
