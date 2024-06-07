import discord
from discord.ext import commands
from discord import app_commands
from PyQt5.QtCore import pyqtSignal, QObject
import json
import os

from utils.saving_loading_json import load_setting_json, save_setting_json


class RewardSystem(commands.Cog):
    # signal to notify the GUI that user data has been modified
    # user_modified = pyqtSignal()

    def __init__(self, bot):
        """
        Initialize the RewardSystem with the bot instance.
        Loads user data from JSON storage.
        """
        self.bot = bot
        self.user_data = load_setting_json('user_data')  # load user data from JSON file

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Triggered whenever a message is sent in any channel the bot has access to.
        Ignores messages sent by bots.
        """
        # if message.author.bot:
        #     return

        user_id = str(message.author.id)
        behaviour_points = len(message.content) * 0.1  # calculate behavior points based on message length

        # Update user data with the message details and calculated points
        self.modify_user(user_id, {
            'is_on_server': True,
            'messages_count': 1,
            'behaviour_points': behaviour_points,
            'reward_points': behaviour_points * 0.1
        })

    @app_commands.command(name="stan_konta", description="Wyświetl stan konta")
    async def stan_konta(self, interaction: discord.Interaction):
        """
        Slash command to display the user's reward points balance.
        """
        self.user_data = load_setting_json('user_data')
        user_points = self.user_data.get(str(interaction.user.id), {}).get('reward_points', 0)
        await interaction.response.send_message(f"Stan Twojego konta: {user_points} punktów")

    async def buy_role(self, interaction: discord.Interaction, role_name: str, cost: int):
        """
        Allows users to buy a role using their reward points.
        """
        self.user_data = load_setting_json('user_data')  # reload user data to ensure it's up to date
        user_points = self.user_data.get(str(interaction.user.id), {}).get('reward_points', 0)
        role = discord.utils.get(interaction.guild.roles, name=role_name) # fetch the role by name
        if role:
            if user_points >= cost:
                self.user_data[str(interaction.user.id)]['reward_points'] -= cost  # deduct the cost
                save_setting_json('user_data', self.user_data) # save updated user data
                await interaction.user.add_roles(role) # assign the role to the user
                await interaction.response.send_message(f"Dodano rolę {role_name}!")
            else:
                await interaction.response.send_message("Nie masz wystarczająco punktów!")
        else:
            await interaction.response.send_message(f"Rola {role_name} nie istnieje!")

    @app_commands.command(name="buy10", description="Kup rolę 10$")
    async def buy10(self, interaction: discord.Interaction):
        """
        Slash command to buy a role priced at 10 points.
        """
        await self.buy_role(interaction, "10$", 10)

    @app_commands.command(name="buy20", description="Kup rolę 20$")
    async def buy20(self, interaction: discord.Interaction):
        """
        Slash command to buy a role priced at 20 points.
        """
        await self.buy_role(interaction, "20$", 20)

    @app_commands.command(name="buy50", description="Kup rolę 50$")
    async def buy50(self, interaction: discord.Interaction):
        """
        Slash command to buy a role priced at 50 points.
        """
        await self.buy_role(interaction, "50$", 50)

    def modify_user(self, user_id, data):
        """
        Update or create user data in storage.
        """
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
    """
    Asynchronous setup function to add this cog to a bot instance.
    """
    await bot.add_cog(RewardSystem(bot))
