import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import datetime

from utils.saving_loading_json import load_setting_json, save_setting_json

class UserModerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.guilds[0]
        self.tree = bot.tree
        self.user_fetcher = bot.get_cog('UserFetcher')
        self.reward_system = bot.get_cog('RewardSystem')

    async def ban_user(self, user_id, reason):
        print(f"banning user {user_id}")
        user = self.guild.get_member(int(user_id))
        self.reward_system.modify_user(int(user.id), {
            'is_on_server': False,
            'behaviour_points': load_setting_json('punishment_settings')['ban'],
            'reward_points': 0
        })
        if user:
            try:
                await user.ban(reason=reason)
                print(f"banned user {user_id}")
                return True
            except discord.Forbidden:
                print(f"Failed to ban user {user_id}")
                return False
            except Exception as e:
                print(f"Error banning user {user_id}: {e}")
                return False
        else:
            print(f"User {user_id} not found.")
            return False

    async def kick_user(self, user_id, reason):
        print(f"kicking user {user_id}")
        user = self.guild.get_member(int(user_id))
        self.reward_system.modify_user(int(user_id), {
            'is_on_server': False,
            'behaviour_points': load_setting_json('punishment_settings')['kick'],
            'reward_points': 0
        })
        if user:
            try:
                await user.kick(reason=reason)
                print(f"kicked user {user_id}")
                return True
            except discord.Forbidden:
                print(f"Failed to kick user {user_id}")
                return False
            except Exception as e:
                print(f"Error kicking user {user_id}: {e}")
                return False
        else:
            print(f"User {user_id} not found.")
            return False

    async def timeout_user(self, user_id, reason, duration):
        print(f"timing out user {user_id}")
        user = self.guild.get_member(int(user_id))
        self.reward_system.modify_user(int(user.id), {
            'behaviour_points': load_setting_json('punishment_settings')['timeout'],
            'reward_points': 0
        })
        if user:
            try:
                until = datetime.datetime.now().astimezone() + datetime.timedelta(seconds=duration)
                await user.timeout(until, reason=reason)
                print(f"timed out user {user_id}")
                return True
            except discord.Forbidden:
                print(f"Failed to time out user {user_id}")
                return False
            except Exception as e:
                print(f"Error timing out user {user_id}: {e}")
                return False
        else:
            print(f"User {user_id} not found.")
            return False

async def setup(bot):
    await bot.add_cog(UserModerator(bot))
