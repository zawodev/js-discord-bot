import discord
from discord.ext import commands
from collections import Counter
import json

class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def backup(self, ctx):
        data = {
            "message_counter": self.bot.get_cog('Statistics').message_counter,
            "user_points": self.bot.get_cog('RewardSystem').user_points,
        }
        with open('backup.json', 'w') as f:
            json.dump(data, f)
        await ctx.send('Backup completed successfully.')

    @commands.command()
    async def restore(self, ctx):
        try:
            with open('backup.json', 'r') as f:
                data = json.load(f)
            self.bot.get_cog('Statistics').message_counter = Counter(data['message_counter'])
            self.bot.get_cog('RewardSystem').user_points = data['user_points']
            await ctx.send('Restore completed successfully.')
        except FileNotFoundError:
            await ctx.send('No backup file found.')

async def setup(bot):
    await bot.add_cog(Backup(bot))
