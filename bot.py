import discord
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the Discord bot token from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

# Set intents for the bot
intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


# Command to create a message with buttons to assign roles
@bot.slash_command(name="create_role_buttons", description="Create a role assignment message")
async def create_role_buttons(ctx, role1: discord.Role, role2: discord.Role):
    embed = discord.Embed(
        title="Role Assignment",
        description="Click the buttons below to get or remove roles.",
        color=discord.Color.blue()
    )

    class RoleView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label=role1.name, style=discord.ButtonStyle.primary, custom_id="role1_button")
        async def role1_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role1 in interaction.user.roles:
                await interaction.user.remove_roles(role1)
                await interaction.response.send_message(f"Removed {role1.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role1)
                await interaction.response.send_message(f"Added {role1.name} role.", ephemeral=True)

        @discord.ui.button(label=role2.name, style=discord.ButtonStyle.primary, custom_id="role2_button")
        async def role2_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role2 in interaction.user.roles:
                await interaction.user.remove_roles(role2)
                await interaction.response.send_message(f"Removed {role2.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role2)
                await interaction.response.send_message(f"Added {role2.name} role.", ephemeral=True)

    await ctx.respond(embed=embed, view=RoleView())


# Command to set a channel for member count updates
@bot.slash_command(name="set_member_count", description="Set a channel to display the member count")
async def set_member_count(ctx, channel: discord.TextChannel):
    async def update_member_count():
        member_count = len(ctx.guild.members)
        message = await fetch_member_count_message(channel)
        if message:
            await message.edit(content=f"Member Count: {member_count}")
        else:
            await channel.send(content=f"Member Count: {member_count}")

    async def fetch_member_count_message(channel):
        async for message in channel.history(limit=100):
            if message.author == bot.user and message.content.startswith("Member Count:"):
                return message
        return None

    @bot.event
    async def on_member_join(member):
        await update_member_count()

    @bot.event
    async def on_member_remove(member):
        await update_member_count()

    await update_member_count()
    await ctx.respond(f"Member count updates set to {channel.mention}")


# Run the bot with the token from the .env file
bot.run(TOKEN)
