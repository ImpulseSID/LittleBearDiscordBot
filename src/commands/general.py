import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Ping the bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong: {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="about", description="About this bot")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Little Bear Discord Music Bot",
            description="A modern, open-source Discord music bot built with discord.py, yt-dlp, and FFmpeg. Supports YouTube playlists, queueing, and more.",
            color=discord.Color.green()
        )
        embed.add_field(
            name="Developer",
            value="ImpulseSID (https://github.com/ImpulseSID)",
            inline=False
        )
        embed.add_field(
            name="Features",
            value=(
                "- Slash commands for all music controls\n"
                "- Play music from YouTube (single tracks & playlists)\n"
                "- Queue, shuffle, skip, and remove tracks\n"
                "- Automatic disconnect when idle\n"
                "- Open source and easy to self-host"
            ),
            inline=False
        )
        embed.add_field(
            name="Source Code",
            value="https://github.com/ImpulseSID/LittleBearDiscordBot",
            inline=False
        )
        embed.set_footer(text="Made with ❤️ by ImpulseSID")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Show help")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Little Bear Music Bot Help", color=discord.Color.blurple())
        embed.add_field(
            name="Music Commands",
            value=(
                "/join [channel] — Join a voice channel\n"
                "/play <url> — Play a single YouTube video or audio URL\n"
                "/queueadd <url> — Add a single YouTube video or audio URL to the queue\n"
                "/playlist <url> — Queue all tracks from a YouTube playlist URL\n"
                "/pause — Pause playback\n"
                "/resume — Resume playback\n"
                "/skip — Skip current track\n"
                "/stop — Stop and clear the queue\n"
                "/queue — Show the current queue\n"
                "/nowplaying — Show the currently playing track\n"
                "/shuffle — Shuffle the queue\n"
                "/clear — Clear the queue\n"
                "/remove <index> — Remove item from queue (1-based)\n"
                "/leave — Leave the voice channel"
            ),
            inline=False
        )
        embed.add_field(
            name="General Commands",
            value="/ping — Ping the bot\n/about — About this bot\n/help — Show help",
            inline=False
        )
        embed.set_footer(text="Made with ❤️ by ImpulseSID")
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))

