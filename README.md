# Python Discord Bot

A Discord bot developed in Python using the `discord.py` library. This bot provides a variety of features for managing a Discord server, including moderation tools and fun commands.

## Features

- **Welcome and Goodbye Messages**: Greets new members and sends a farewell message when they leave the server.
- **YouTube Notifications**: Sends notifications to the server when new videos are uploaded to a specific YouTube channel using the YouTube API.
- **Banned Words Enforcement**: Automatically times out users who use banned words in messages.
- **Reward and Penalty System**: Tracks user karma and assigns rewards or penalties based on behavior. Users with low karma may face punishments.
- **Server Statistics**: Displays various server statistics, such as total members, active users, and more.
- **User Moderation**: Provides moderation tools for kicking, banning, and managing users based on behavior.

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

### Running the Application

To start the app, simply run:
```bash
python main.py
```

## Usage

Here’s an overview of the key functionalities your bot provides:

- **Welcome/Goodbye Messages**: The bot will automatically send a welcome message when a new user joins and a goodbye message when they leave the server.
  
- **YouTube Notifications**: The bot will monitor a YouTube channel and post a notification to a designated channel when new videos are uploaded.

- **Banned Words Enforcement**: The bot tracks a list of banned words, and if any user sends a message containing them, they will be temporarily timed out.

- **Reward System**: Each user has a karma score, and based on their behavior, they can gain or lose points. Negative karma may result in punishments like mutes or bans, while positive behavior is rewarded.

- **Server Statistics**: The bot can display stats about server usage, such as the number of active users, total members, and message counts.

- **Moderation Tools**: Allows moderators to manage users with commands such as `kick`, `ban`, and `mute`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or issues, feel free to open an issue in this repository.
