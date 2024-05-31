import discord
from discord import app_commands
from discord.ext import commands
from utils.banned_words import load_banned_words
from urlextract import URLExtract
from utils.settings import load_setting


def contains_link(message):
    extractor = URLExtract()
    links = extractor.find_urls(message)
    return len(links) > 0


class BannedWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # banned words
        banned_words = load_banned_words()

        # check for links
        check_for_links = load_setting("check_for_links").lower() == "true"

        # if any banned words are in the message, delete the message
        if any(bad_word in message.content for bad_word in banned_words):
            await message.delete()
            await message.channel.send(f'{message.author.mention}, your message was deleted due to inappropriate content.')

        # check for links
        if check_for_links and contains_link(message.content):
            await message.delete()
            await message.channel.send(f'{message.author.mention}, your message was deleted due to containing a link.')

async def setup(bot):
    await bot.add_cog(BannedWords(bot))
