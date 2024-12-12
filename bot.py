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
async def create_role_buttons(ctx,
                               role1: discord.Role, role2: discord.Role, role3: discord.Role,
                               role4: discord.Role, role5: discord.Role, role6: discord.Role,
                               role7: discord.Role, role8: discord.Role, role9: discord.Role,
                               role10: discord.Role):
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

        @discord.ui.button(label=role3.name, style=discord.ButtonStyle.primary, custom_id="role3_button")
        async def role3_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role3 in interaction.user.roles:
                await interaction.user.remove_roles(role3)
                await interaction.response.send_message(f"Removed {role3.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role3)
                await interaction.response.send_message(f"Added {role3.name} role.", ephemeral=True)

        @discord.ui.button(label=role4.name, style=discord.ButtonStyle.primary, custom_id="role4_button")
        async def role4_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role4 in interaction.user.roles:
                await interaction.user.remove_roles(role4)
                await interaction.response.send_message(f"Removed {role4.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role4)
                await interaction.response.send_message(f"Added {role4.name} role.", ephemeral=True)

        @discord.ui.button(label=role5.name, style=discord.ButtonStyle.primary, custom_id="role5_button")
        async def role5_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role5 in interaction.user.roles:
                await interaction.user.remove_roles(role5)
                await interaction.response.send_message(f"Removed {role5.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role5)
                await interaction.response.send_message(f"Added {role5.name} role.", ephemeral=True)

        @discord.ui.button(label=role6.name, style=discord.ButtonStyle.primary, custom_id="role6_button")
        async def role6_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role6 in interaction.user.roles:
                await interaction.user.remove_roles(role6)
                await interaction.response.send_message(f"Removed {role6.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role6)
                await interaction.response.send_message(f"Added {role6.name} role.", ephemeral=True)

        @discord.ui.button(label=role7.name, style=discord.ButtonStyle.primary, custom_id="role7_button")
        async def role7_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role7 in interaction.user.roles:
                await interaction.user.remove_roles(role7)
                await interaction.response.send_message(f"Removed {role7.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role7)
                await interaction.response.send_message(f"Added {role7.name} role.", ephemeral=True)

        @discord.ui.button(label=role8.name, style=discord.ButtonStyle.primary, custom_id="role8_button")
        async def role8_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role8 in interaction.user.roles:
                await interaction.user.remove_roles(role8)
                await interaction.response.send_message(f"Removed {role8.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role8)
                await interaction.response.send_message(f"Added {role8.name} role.", ephemeral=True)

        @discord.ui.button(label=role9.name, style=discord.ButtonStyle.primary, custom_id="role9_button")
        async def role9_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role9 in interaction.user.roles:
                await interaction.user.remove_roles(role9)
                await interaction.response.send_message(f"Removed {role9.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role9)
                await interaction.response.send_message(f"Added {role9.name} role.", ephemeral=True)

        @discord.ui.button(label=role10.name, style=discord.ButtonStyle.primary, custom_id="role10_button")
        async def role10_button(self, button: discord.ui.Button, interaction: discord.Interaction):
            if role10 in interaction.user.roles:
                await interaction.user.remove_roles(role10)
                await interaction.response.send_message(f"Removed {role10.name} role.", ephemeral=True)
            else:
                await interaction.user.add_roles(role10)
                await interaction.response.send_message(f"Added {role10.name} role.", ephemeral=True)

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
