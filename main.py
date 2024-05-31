import sys
import threading
from discord_bot.bot import DiscordBot
from control_app.app import BotControlApp


if __name__ == '__main__':
    # create an event to signal when the bot is ready
    ready_event = threading.Event()

    # start the discord bot
    bot = DiscordBot(ready_event)
    bot_thread = threading.Thread(target=bot.run)
    bot_thread.start()

    # wait for the bot to be ready
    ready_event.wait()

    # start the control panel
    app = BotControlApp(sys.argv, bot.get_bot())
    app.run()
