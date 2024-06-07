import discord
from discord.ext import commands, tasks
from utils.saving_loading_json import load_setting_json, save_setting_json
import utils.youtube_api_handler as yt_api

from utils.format_message import format_message

class ExternalAPI(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the ExternalAPI cog with default settings and video information.
        """
        self.bot = bot
        self.guild = bot.guilds[0]  # reference to the first guild the bot is part of
        self.youtube_channel_name_or_url = None  # YouTube channel details
        self.discord_channel_name = None  # Discord channel for notifications
        self.notification_message = None  # Message format for notifications
        self.video_info = None  # Store latest video info

        self.update_settings()  # Load initial settings from JSON

    @property
    def video_url(self):
        """
        Constructs a URL for the YouTube video from stored video ID.
        """
        return f"https://www.youtube.com/watch?v={self.video_info['id']['videoId']}"

    def update_settings(self):
        """
        Loads settings from a JSON file, updating cog's configuration.
        """
        try:
            settings = load_setting_json('api_integration_settings')
            self.youtube_channel_name_or_url = settings['youtube_channel_name_or_url']
            self.discord_channel_name = settings['discord_channel_name']
            self.notification_message = settings['notification_message']
            self.video_info = load_setting_json('video_info')
        except Exception as e:
            print(f'Failed to load settings: {e}')

    async def send_notification(self):
        """
        Sends a formatted notification message to a specified Discord channel.
        """
        channel = discord.utils.get(self.guild.text_channels, name=self.discord_channel_name)
        if channel:
            changes = {
                '{author}': self.video_info['snippet']['channelTitle'],
                '{title}': self.video_info['snippet']['title']
            }
            message = f'{format_message(self.notification_message, changes)} {self.video_url}'
            await channel.send(message)

    def check_for_new_video(self):
        """
        Checks for new videos and triggers a notification if a new video is found.
        """
        is_new_vid = self.update_latest_video_link()
        if is_new_vid:
            self.bot.loop.create_task(self.send_notification())

    @tasks.loop(minutes=15)
    async def check_for_new_videos(self):
        """
        Periodically checks for new videos every 15 minutes.
        """
        is_new_vid = self.update_latest_video_link()
        if is_new_vid:
            await self.send_notification()

    def update_latest_video_link(self):
        """
        Updates stored video information if a new video is found.
        """
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
    """
    Standard asynchronous setup function to add this cog to a bot instance.
    """
    await bot.add_cog(ExternalAPI(bot))
