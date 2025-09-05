import asyncio
import discord
from discord.ext import commands

import config
import commands.music as music
import commands.general as general

intents = discord.Intents.default()
intents.message_content = config.INTENTS_MESSAGE_CONTENT
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands globally")
    except Exception as e:
        print(f"Sync failed: {e}")
    print(f"Logged in as {bot.user}")

async def main():
    async with bot:
        await music.setup(bot)
        await general.setup(bot)
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
