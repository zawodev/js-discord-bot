import discord
from discord import app_commands
from discord.ext import commands
from urlextract import URLExtract
from utils.saving_loading_json import load_setting_json

def contains_link(message):
    """
    Check if the message contains any URLs.
    Uses the URLExtract library to find URLs within a string.
    """
    extractor = URLExtract()
    links = extractor.find_urls(message)
    return len(links) > 0  # return True if there is at least one URL

class BannedWords(commands.Cog):
    def __init__(self, bot):
        """
        Initialize the BannedWords cog with a reference to the bot and its command tree.
        Accesses the RewardSystem cog for modifying user points.
        """
        self.bot = bot
        self.tree = bot.tree
        self.reward_system = bot.get_cog('RewardSystem')  # get instance of RewardSystem cog

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listener for any message sent in a channel that the bot has access to.
        Checks messages for banned words and URLs based on settings.
        """
        if message.author == self.bot.user:  # avoid processing messages sent by the bot itself
            return

        # Load banned words from JSON file
        banned_words = []
        try:
            banned_words = load_setting_json('banned_words')
        except Exception as e:
            print(f'Failed to load banned words: {e}')  # log if there's an error loading the banned words

        # Load settings for checking links
        check_for_links = load_setting_json("banned_words_settings")["check_for_links"].lower() == "true"

        # Delete message if it contains any banned words
        if any(bad_word in message.content for bad_word in banned_words):
            await message.delete()
            self.reward_system.modify_user(str(message.author.id), {
                'behaviour_points': -25.52,  # apply a penalty to behavior points
                'reward_style': 0  # no change to reward points
            })
            await message.channel.send(f'{message.author.mention}, your message was deleted due to inappropriate content.')

        # Delete message if it contains links and the setting is enabled
        if check_for_links and contains_link(message.content):
            await message.delete()
            self.reward_system.modify_user(str(message.author.id), {
                'behaviour_points': -32.29,  # apply a penalty to behavior points
                'reward_points': 0  # no change to reward points
            })
            await message.channel.send(f'{message.author.mention}, your message was deleted due to containing a link.')

async def setup(bot):
    """
    Asynchronous setup function to add this cog to a bot instance.
    """
    await bot.add_cog(BannedWords(bot))
