# Python Discord Bot

A Discord bot developed in Python using the `discord.py` library. This bot provides a variety of features for managing a Discord server, including moderation tools and fun commands.

## Features

- **Moderation Commands**: Kick, ban, mute commands for server management.
- **Fun Commands**: Engage users with features like random jokes, rolling dice, and more.
- **Customizable**: Easily add new commands or modify existing ones.
- **Event Handlers**: React to different server events (e.g., new member joins).

## Requirements

- Python 3.8+
- `discord.py` library
- A Discord bot token (from the [Discord Developer Portal](https://discord.com/developers/applications))

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/zawodev/js-discord-bot.git
   ```

2. Navigate to the project directory:
   ```bash
   cd js-discord-bot
   ```

3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file and add your bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```

### Running the Bot

To start the bot, simply run:
```bash
python bot.py
```

## Usage

Once the bot is running, it can respond to various commands such as:

- `!ping`: Responds with "Pong!"
- `!kick @user`: Kicks a user from the server.
- `!ban @user`: Bans a user from the server.
- `!roll [number]`: Rolls a dice with the specified number of sides.

You can add more commands by editing the `cogs` directory.

## Contributing

Contributions are welcome! If you would like to contribute, please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/my-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add my feature'`).
5. Push to the branch (`git push origin feature/my-feature`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or issues, feel free to open an issue in this repository.
