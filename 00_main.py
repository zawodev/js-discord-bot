import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

load_dotenv()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    await load_extensions()
    print(f'Loaded {len(bot.cogs)} cogs')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # await bot.process_commands(message) # this is not needed
    # await message.channel.send("Hello, world!")

@bot.tree.command(name="example_command")
@app_commands.describe(custom_argument="put argument description here")
async def example_command(ctx: discord.Interaction, custom_argument: str):
    await ctx.response.send_message("success")

bot.run(os.getenv("DISCORD_TOKEN"))
