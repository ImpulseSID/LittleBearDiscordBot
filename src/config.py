import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

INTENTS_MESSAGE_CONTENT = True

FFMPEG_BEFORE_OPTS = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin"
FFMPEG_OPTIONS = "-vn"

YDL_FORMAT = "bestaudio/best"
YDL_DEFAULT_SEARCH = "ytsearch"
YDL_NPLAYLIST = True
