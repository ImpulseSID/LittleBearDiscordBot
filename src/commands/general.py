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
        embed = discord.Embed(title="Discord Music Bot", description="Slash-command music bot using yt-dlp and ffmpeg.")
        embed.add_field(name="Commands", value="/join /play /pause /resume /skip /stop /queue /nowplaying /shuffle /clear /remove /leave /ping /help", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="Show help")
    async def help(self, interaction: discord.Interaction):
        text = (
            "**Music**\n"
            "/join [channel] — Join a voice channel\n"
            "/play <query|url> — Add a track to the queue and play\n"
            "/pause — Pause\n"
            "/resume — Resume\n"
            "/skip — Skip current\n"
            "/stop — Stop and clear queue\n"
            "/queue — Show queue\n"
            "/nowplaying — Show current track\n"
            "/shuffle — Shuffle the queue\n"
            "/clear — Clear the queue\n"
            "/remove <index> — Remove item from queue (1-based)\n"
            "/leave — Leave voice channel\n\n"
            "**General**\n"
            "/ping, /about, /help"
        )
        await interaction.response.send_message(text)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))

