import discord
from discord.ext import commands
from utils.saving_loading_json import save_setting_json, load_setting_json

class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def collect_data(self):
        messages_data = {}
        channel_data = {}
        print("Collecting data...")

        for guild in self.bot.guilds:
            for member in guild.members:
                messages_data[member.id] = 0
            print(f"Collected data for {guild.name} members.")
            for channel in guild.text_channels:
                channel_data[channel.id] = {
                    "messages_count": 0,
                    "name": channel.name
                }
                async for message in channel.history(limit=None):
                    if message.author.id in messages_data:
                        messages_data[message.author.id] += 1
                    if channel.id in channel_data:
                        channel_data[channel.id]["messages_count"] += 1
            print(f"Collected data for {guild.name} channels.")

        self.modify_users("user_data", messages_data)
        save_setting_json("channel_stats", channel_data)

    def modify_users(self, key, messages_data):
        data = load_setting_json(key)
        for user_id, messages_count in messages_data.items():
            if user_id in data:
                data[str(user_id)]["messages_count"] += messages_count
            else:
                data[str(user_id)]["messages_count"] = messages_count
        save_setting_json(key, data)

async def setup(bot):
    await bot.add_cog(Statistics(bot))
