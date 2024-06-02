import discord
from discord import app_commands
from discord.ext import commands
from urlextract import URLExtract
from utils.saving_loading_json import load_setting_json


def contains_link(message):
    extractor = URLExtract()
    links = extractor.find_urls(message)
    return len(links) > 0


class BannedWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree
        self.reward_system = bot.get_cog('RewardSystem')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # banned words
        banned_words = []
        try:
            banned_words = load_setting_json('banned_words')
        except Exception as e:
            print(f'Failed to load banned words: {e}')

        # check for links
        check_for_links = load_setting_json("banned_words_settings")["check_for_links"].lower() == "true"

        # if any banned words are in the message, delete the message
        if any(bad_word in message.content for bad_word in banned_words):
            await message.delete()
            self.reward_system.modify_user(str(message.author.id), {
                'behaviour_points': -25.52,
                'reward_points': 0
            })
            await message.channel.send(f'{message.author.mention}, your message was deleted due to inappropriate content.')

        # check for links
        if check_for_links and contains_link(message.content):
            await message.delete()
            self.reward_system.modify_user(str(message.author.id), {
                'behaviour_points': -32.29,
                'reward_points': 0
            })
            await message.channel.send(f'{message.author.mention}, your message was deleted due to containing a link.')

async def setup(bot):
    await bot.add_cog(BannedWords(bot))
