import discord
from discord.ext import commands
import config
from utils.auto_update import AutoUpdate

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs dynamically
async def load_cogs():
    await bot.load_extension("cogs.leaderboard")  # Load leaderboard commands

@bot.event
async def on_ready():
    """Handles bot startup and starts auto-updating leaderboard."""
    print(f"✅ Logged in as {bot.user}")
    print("🔄 Checking for command updates...")
    await bot.tree.sync()
    print("✅ Slash commands synced successfully!")

    # Start the leaderboard auto-update task
    bot.auto_update = AutoUpdate(bot)
    bot.auto_update.start()

bot.run(config.TOKEN)