import discord
from PyQt5.QtWidgets import QMessageBox
from discord.ext import commands
from utils.saving_loading_json import save_setting_json, load_setting_json

class FetchData(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.guilds[0]

    async def collect_data(self):
        # messages_data = {}
        channel_data = {}
        user_data = load_setting_json("user_data")
        print("Collecting data...")

        for key in user_data.keys():
            user_data[key]['is_on_server'] = False

        for member in self.guild.members:
            # messages_data[member.id] = 0
            user_data[str(member.id)]['messages_count'] = 0
            user_data[str(member.id)]['is_on_server'] = True
            user_data[str(member.id)]['name'] = member.name
            user_data[str(member.id)]['avatar_url'] = str(member.avatar.url)
        print(f"Collected data for {self.guild.name} members.")

        for channel in self.guild.text_channels:
            channel_data[channel.id] = {
                "messages_count": 0,
                "name": channel.name
            }
            async for message in channel.history(limit=None):
                if str(message.author.id) in user_data:
                    user_data[str(message.author.id)]['messages_count'] += 1
                else:
                    user_data[str(message.author.id)] = {
                        'behaviour_points': 0,
                        'reward_points': 0,
                        'messages_count': 1,
                        'is_on_server': False,
                        'name': message.author.name,
                        'avatar_url': str(message.author.avatar.url)
                    }
                if channel.id in channel_data:
                    channel_data[channel.id]["messages_count"] += 1
        print(f"Collected data for {self.guild.name} channels.")

        save_setting_json("user_data", user_data)
        save_setting_json("channel_stats", channel_data)


async def setup(bot):
    await bot.add_cog(FetchData(bot))
