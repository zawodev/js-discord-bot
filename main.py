import sys
import threading
from discord_bot.bot import DiscordBot
from control_app.app import BotControlApp


if __name__ == '__main__':
    # start the discord bot
    bot = DiscordBot()
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.start()

    # start the control panel
    app = BotControlApp(sys.argv, bot.get_bot())
    app.run()
