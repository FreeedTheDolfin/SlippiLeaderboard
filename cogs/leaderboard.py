import discord
from discord import app_commands, Interaction  # Ensure Interaction is imported correctly
from discord.ext import commands
from utils.data_manager import load_data, save_data
from utils.image_generator import generate_leaderboard_image
from slippy.api import fetch_player_data

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()
        self.leaderboard = self.data["leaderboard"]
        self.channel_id = self.data["channel_id"]
        self.last_message_id = self.data["last_leaderboard_message_id"]

    @app_commands.command(name="sl1ppi_setchannel", description="Sets the leaderboard channel.")
    @app_commands.describe(channel_name="The name of the text channel where leaderboard updates will be posted.")
    async def setchannel(self, interaction: Interaction, channel_name: str):
        """Sets the leaderboard update channel."""
        channel = discord.utils.get(interaction.guild.text_channels, name=channel_name)

        if channel:
            self.channel_id = channel.id
            save_data(self.leaderboard, self.channel_id, self.last_message_id)
            await interaction.response.send_message(f"✅ Leaderboard updates will be posted in {channel.mention}.")
        else:
            await interaction.response.send_message("⚠️ No such channel found!", ephemeral=True)

    @app_commands.command(name="sl1ppi_add", description="Adds a player to the leaderboard.")
    @app_commands.describe(slippi_code="The player's Slippi code (e.g., FRED#282).")
    async def add(self, interaction: Interaction, slippi_code: str):
        """Adds a player to the leaderboard."""
        await interaction.response.defer(thinking=True)
        player = fetch_player_data(slippi_code)

        if not player:
            await interaction.followup.send("❌ Player not found or has no ranked data!")
            return

        if any(p["code"] == slippi_code for p in self.leaderboard):
            await interaction.followup.send(f"⚠️ {slippi_code} is already on the leaderboard!", ephemeral=True)
            return

        self.leaderboard.append(player)
        self.leaderboard.sort(key=lambda x: x["elo"], reverse=True)
        save_data(self.leaderboard, self.channel_id, self.last_message_id)

        await interaction.followup.send(f"✅ Added {player['username']} ({player['elo']} ELO)")

    @app_commands.command(name="sl1ppi_remove", description="Removes a player from the leaderboard.")
    @app_commands.describe(slippi_code="The player's Slippi code to remove.")
    async def remove(self, interaction: Interaction, slippi_code: str):
        """Removes a player from the leaderboard."""
        await interaction.response.defer(thinking=True)

        for player in self.leaderboard:
            if player["code"].lower() == slippi_code.lower():
                self.leaderboard.remove(player)
                save_data(self.leaderboard, self.channel_id, self.last_message_id)
                await interaction.followup.send(f"❌ Removed {player['username']} ({player['code']}) from the leaderboard.")
                return

        await interaction.followup.send(f"⚠️ Player {slippi_code} not found.")

    @app_commands.command(name="sl1ppi_leaderboard", description="Displays the leaderboard.")
    @app_commands.describe(update="Whether or not to fetch updated data from the Slippi API.")
    async def leaderboard(self, interaction: Interaction, update: bool = False):
        """Displays the Slippi leaderboard with an option to fetch updated data."""
        await interaction.response.defer(thinking=True)
    
        if not self.leaderboard:
            await interaction.followup.send("🏆 No players in the leaderboard yet!")
            return
    
        # If update is True, fetch the latest player data from the Slippi API
        if update:
            updated_leaderboard = []
            for player in self.leaderboard:
                try:
                    player_data = fetch_player_data(player["code"])
                    if player_data:
                        updated_leaderboard.append(player_data)
                except Exception as e:
                    print(f"❌ Error updating player {player['code']}: {e}")
                    continue
                
            if updated_leaderboard:
                self.leaderboard.clear()
                self.leaderboard.extend(updated_leaderboard)
                self.leaderboard.sort(key=lambda x: x["elo"], reverse=True)
                save_data(self.leaderboard, self.channel_id, self.last_message_id)
                generate_leaderboard_image(self.leaderboard)
                await interaction.followup.send("✅ Leaderboard updated from the Slippi API!", ephemeral=True)
            else:
                await interaction.followup.send("⚠️ No updated player data available.", ephemeral=True)
    
        else:
            generate_leaderboard_image(self.leaderboard)
            await interaction.followup.send("✅ Displaying saved leaderboard.", ephemeral=True)
    
        # Get the target channel (use the saved channel if available)
        channel = self.bot.get_channel(self.channel_id) or interaction.channel
    
        # Delete previous leaderboard message if it exists
        if self.last_message_id:
            try:
                old_msg = await channel.fetch_message(self.last_message_id)
                await old_msg.delete()
            except discord.NotFound:
                pass
            
        # Send the updated leaderboard image
        leaderboard_message = await channel.send(file=discord.File("leaderboard.png"))
        self.last_message_id = leaderboard_message.id
        save_data(self.leaderboard, self.channel_id, self.last_message_id)
    
        await interaction.followup.send("✅ Leaderboard updated!", ephemeral=True)

    @app_commands.command(name="sl1ppi_resetleaderboard", description="Resets the leaderboard.")
    @app_commands.describe(confirm="Type 'confirm' to reset the leaderboard.")
    async def resetleaderboard(self, interaction: Interaction, confirm: str):
        """Clears the leaderboard after confirmation."""
        if confirm.lower() != "confirm":
            await interaction.response.send_message("⚠️ You must type 'confirm' to reset the leaderboard.", ephemeral=True)
            return

        await interaction.response.defer(thinking=True)

        self.leaderboard.clear()
        save_data(self.leaderboard, self.channel_id, self.last_message_id)

        await interaction.followup.send("✅ Leaderboard has been reset!")

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))