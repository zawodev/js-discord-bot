import discord
from PyQt5.QtWidgets import QMessageBox
from discord.ext import commands
from utils.saving_loading_json import save_setting_json, load_setting_json

class FetchData(commands.Cog):
    def __init__(self, bot):
        """
        Initialize the FetchData cog with references to the bot and settings from JSON.
        """
        self.bot = bot
        self.guild = bot.guilds[0]  # assuming the bot is only part of one guild
        self.logs_channel = load_setting_json("app_settings")["bot_logs_channel"]  # load logs channel ID from settings

    async def collect_data(self):
        """
        Collects and updates data for all guild members and channels.
        Updates user message counts and membership status.
        """
        channel_data = {}
        user_data = load_setting_json("user_data")  # load existing user data from JSON
        print("Collecting data...")

        # Reset user presence status
        for key in user_data.keys():
            user_data[key]['is_on_server'] = False  # mark all users as initially not on the server

        # Update member data
        for member in self.guild.members:
            user_data[str(member.id)]['messages_count'] = 0  # reset message count to 0
            user_data[str(member.id)]['is_on_server'] = True  # update presence status
            user_data[str(member.id)]['name'] = member.name  # store member's name
            user_data[str(member.id)]['avatar_url'] = str(member.avatar.url)  # store URL to member's avatar
        print(f"Collected data for {self.guild.name} members.")

        # Update channel and message data
        for channel in self.guild.text_channels:
            channel_data[channel.id] = {
                "messages_count": 0,  # initialize message count for each channel
                "name": channel.name  # store channel name
            }
            # Collect message data by iterating through each message in channel history
            async for message in channel.history(limit=None):
                if str(message.author.id) in user_data:
                    user_data[str(message.author.id)]['messages_count'] += 1  # increment message count
                else:
                    # Initialize data for new user found in message history
                    user_data[str(message.author.id)] = {
                        'behaviour_points': 0,
                        'reward_points': 0,
                        'messages_count': 1,
                        'is_on_server': False,  # user not set as being on server initially
                        'name': message.author.name,
                        'avatar_url': str(message.author.avatar.url)
                    }
                if channel.id in channel_data:
                    channel_data[channel.id]["messages_count"] += 1  # increment channel message count
        print(f"Collected data for {self.guild.name} channels.")

        # Optionally send a log message via another cog's method
        settings_cog = self.bot.get_cog('Settings')
        self.bot.loop.create_task(settings_cog.send_log(self.logs_channel, f"Collected data for {self.guild.name} members and channels."))
        save_setting_json("user_data", user_data)  # save the updated user data to JSON
        save_setting_json("channel_stats", channel_data)  # save channel statistics to JSON

async def setup(bot):
    """
    Standard asynchronous setup function to add this cog to a bot instance.
    """
    await bot.add_cog(FetchData(bot))
