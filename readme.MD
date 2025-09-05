# LittleBear Discord Music Bot

A modern, slash-command-based Discord music bot built with [discord.py](https://github.com/Rapptz/discord.py), [yt-dlp](https://github.com/yt-dlp/yt-dlp), and FFmpeg. Supports YouTube and other sources, queueing, shuffling, and more.

---

## Features

- **Slash Commands**: All controls via Discord's modern slash commands.
- **Music Playback**: Play music from YouTube and other sources using yt-dlp.
- **Queue System**: Add, remove, shuffle, and clear tracks in the queue.
- **Voice Channel Management**: Join, leave, and move between voice channels.
- **Playback Controls**: Pause, resume, skip, and stop playback.
- **Now Playing**: See what's currently playing.
- **Help & About**: Built-in help and about commands.

---

## Commands
```sh
| Command           | Description                              |
| ----------------- | ---------------------------------------- |
| `/join [channel]` | Join a voice channel (or user's current) |
| `/play <queryurl>`| Add a track to the queue and play        |
| `/pause`          | Pause playback                           |
| `/resume`         | Resume playback                          |
| `/skip`           | Skip the current track                   |
| `/stop`           | Stop and clear the queue                 |
| `/queue`          | Show the current queue                   |
| `/nowplaying`     | Show the currently playing track         |
| `/shuffle`        | Shuffle the queue                        |
| `/clear`          | Clear the queue                          |
| `/remove <index>` | Remove item from queue (1-based)         |
| `/leave`          | Leave the voice channel                  |
| `/ping`           | Ping the bot                             |
| `/about`          | About this bot                           |
| `/help`           | Show help                                |
```
---

## Setup & Installation

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/LittleBearDiscordBot.git
cd LittleBearDiscordBot
```

### 2. Install Python Dependencies

Make sure you have Python 3.11+ installed.

```sh
pip install -r requirements.txt
```

### 3. Install FFmpeg

- Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system PATH.

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```
DISCORD_TOKEN=your_discord_bot_token_here
```

### 5. Run the Bot

```sh
python -m src.bot
```

---

## Folder Structure

```
LittleBearDiscordBot/
├── src/
│   ├── bot.py           # Main bot entrypoint
│   ├── config.py        # Configuration and environment
│   ├── commands/
│   │   ├── music.py     # Music commands and logic
│   │   └── general.py   # General commands (ping, help, about)
│   └── utils/
│       └── yt_dlp_handler.py # yt-dlp integration
├── requirements.txt     # Python dependencies
├── .env                 # Your Discord bot token (not committed)
└── readme.MD            # This file
```

---

## Permissions

When inviting your bot, ensure it has the following permissions:

- Connect
- Speak
- View Channels
- Use Slash Commands

---

## Troubleshooting

- **Bot not joining VC?**
  - Check bot permissions in the server and channel.
  - Ensure FFmpeg is installed and in your PATH.
  - Check the console for error logs (extensive logging is included).
- **Music not playing?**
  - Make sure the bot is in a voice channel.
  - Check if the provided URL/query is valid.
  - Ensure yt-dlp is up to date.

---

## Credits

- [discord.py](https://github.com/Rapptz/discord.py)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)

---

## License

MIT License. See `LICENSE`
