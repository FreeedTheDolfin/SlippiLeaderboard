import asyncio
import discord
from discord.ext import tasks
from utils.data_manager import load_data, save_data
from utils.image_generator import generate_leaderboard_image
from slippy.api import fetch_player_data
from config import AUTO_UPDATE_INTERVAL

class AutoUpdate:
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()
        self.leaderboard = self.data["leaderboard"]
        self.channel_id = self.data["channel_id"]
        self.last_message_id = self.data["last_leaderboard_message_id"]

    @tasks.loop(minutes=AUTO_UPDATE_INTERVAL)
    async def auto_update_task(self):
        """Automatically updates the leaderboard every X minutes."""
        if not self.channel_id:
            print("⚠️ Auto-update skipped: No leaderboard channel set.")
            return

        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print("⚠️ Auto-update skipped: Leaderboard channel not found.")
            return

        print("🔄 Auto-updating leaderboard...")

        updated_leaderboard = []
        for player in self.leaderboard:
            try:
                # Fetch updated data from the Slippi API
                player_data = fetch_player_data(player["code"])
                if player_data:
                    updated_leaderboard.append(player_data)
            except Exception as e:
                print(f"❌ Error updating player {player['code']}: {e}")
                continue  # Skip any players that can't be updated

        if not updated_leaderboard:
            print("⚠️ Auto-update skipped: No valid player data.")
            return

        # Replace leaderboard with updated data
        self.leaderboard.clear()
        self.leaderboard.extend(updated_leaderboard)
        self.leaderboard.sort(key=lambda x: x["elo"], reverse=True)
        save_data(self.leaderboard, self.channel_id, self.last_message_id)

        # Generate the updated leaderboard image
        generate_leaderboard_image(self.leaderboard)

        # Delete the old leaderboard message
        if self.last_message_id:
            try:
                last_message = await channel.fetch_message(self.last_message_id)
                await last_message.delete()
                print("✅ Deleted previous leaderboard message.")
            except discord.NotFound:
                pass  # If the message was already deleted

        # Send the new leaderboard image
        new_message = await channel.send(file=discord.File("leaderboard.png"))
        self.last_message_id = new_message.id
        save_data(self.leaderboard, self.channel_id, self.last_message_id)

        print("✅ Leaderboard auto-updated!")

    def start(self):
        """Starts the auto-update task when the bot is ready."""
        if not self.auto_update_task.is_running():
            print("✅ Starting auto-update loop...")
            self.auto_update_task.start()