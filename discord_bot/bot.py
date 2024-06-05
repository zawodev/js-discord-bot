import os
from dotenv import load_dotenv
import threading

import discord
from discord import app_commands
from discord.ext import commands

from utils.saving_loading_json import load_setting_json


class DiscordBot:
    def __init__(self, _ready_event, command_prefix='/', intents=discord.Intents.all()):
        load_dotenv()
        self.ready_event = _ready_event
        self.bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)
        self.bot.tree.command(name="test")(self.test)

    async def load_extensions(self):
        for filename in os.listdir('discord_bot/cogs'):
            if filename.endswith('.py'):
                await self.bot.load_extension(f'discord_bot.cogs.{filename[:-3]}')

    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} ({self.bot.user.id})')
        await self.load_extensions()
        print(f'Loaded {len(self.bot.cogs)} cogs')
        #try:
            #synced = await self.bot.tree.sync()
            #print(f"Synced {len(synced)} commands")
        #except Exception as e:
            #print(f"Failed to sync commands: {e}")

        self.ready_event.set()

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        # process other messages if needed
        # await self.bot.process_commands(message) # uncomment if you want to process commands

    def get_bot(self):
        return self.bot

    @app_commands.describe(custom_argument="put argument description here")
    async def test(self, ctx: discord.Interaction, custom_argument: str):
        await ctx.response.send_message("success")

    def run(self):
        settings_token = load_setting_json("app_settings")['discord_api_key']
        if len(settings_token) == 72:
            self.bot.run(settings_token)
        else:
            self.bot.run(os.getenv("DISCORD_TOKEN"))


# if this module is run directly, create and run the bot
if __name__ == "__main__":
    ready_event = threading.Event()
    bot_instance = DiscordBot(ready_event)
    bot_instance.run()
