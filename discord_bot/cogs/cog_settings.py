import json

import discord
from discord.ext import commands, tasks

from utils.saving_loading_json import load_setting_json, save_setting_json

import utils.youtube_api_handler as yt_api

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.app_settings = load_setting_json("app_settings")

        self.guild = None
        self.update_guild()

        self.send_start_message()

    def send_start_message(self):
        if self.app_settings.get("bot_start_message") and self.app_settings.get("bot_logs_channel"):
            start_message = self.app_settings.get("bot_start_message")
            channel_name = self.app_settings.get("bot_logs_channel")
            self.bot.loop.create_task(self.send_log(channel_name, start_message))

    def update_guild(self):
        try:
            guild_id = int(self.app_settings["discord_guild_id"])
            self.guild = discord.utils.get(self.bot.guilds, id=guild_id)
        except Exception as e:
            print(f"Failed to load guild: {e}")

    async def send_log(self, channel_name, message):
        if channel_name and message:
            channel = discord.utils.get(self.guild.text_channels, name=channel_name)
            if channel:
                await channel.send(message)

async def setup(bot):
    await bot.add_cog(Settings(bot))
