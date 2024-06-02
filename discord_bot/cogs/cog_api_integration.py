import json

import discord
from discord.ext import commands, tasks

from utils.saving_loading_json import load_setting_json, save_setting_json

import utils.youtube_api_handler as yt_api

class ExternalAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.guilds[0]
        self.youtube_channel_name_or_url = None
        self.discord_channel_name = None
        self.notification_message = None
        self.video_info = None

        self.update_settings()

    @property
    def video_url(self):
        return f"https://www.youtube.com/watch?v={self.video_info['id']['videoId']}"

    def update_settings(self):
        try:
            settings = load_setting_json('api_integration_settings')
            self.youtube_channel_name_or_url = settings['youtube_channel_name_or_url']
            self.discord_channel_name = settings['discord_channel_name']
            self.notification_message = settings['notification_message']
            self.video_info = load_setting_json('video_info')
        except Exception as e:
            print(f'Failed to load settings: {e}')

    async def send_notification(self):
        channel = discord.utils.get(self.guild.text_channels, name=self.discord_channel_name)
        if channel:
            message = f'{self.notification_message} {self.video_url}'
            await channel.send(message)

    def check_for_new_video(self):
        is_new_vid = self.update_latest_video_link()
        if is_new_vid:
            self.bot.loop.create_task(self.send_notification())

    @tasks.loop(minutes=15)
    async def check_for_new_videos(self):
        is_new_vid = self.update_latest_video_link()
        if is_new_vid:
            await self.send_notification()

    def update_latest_video_link(self):
        new_video_info = yt_api.get_latest_video_info(self.youtube_channel_name_or_url)
        if new_video_info != self.video_info:
            self.video_info = new_video_info
            try:
                save_setting_json('video_info', new_video_info)
            except Exception as e:
                print(f'Failed to save video info: {e}')
            return True
        return False

async def setup(bot):
    await bot.add_cog(ExternalAPI(bot))
