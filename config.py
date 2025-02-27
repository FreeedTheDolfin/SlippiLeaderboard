import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DATA_FILE = "data.json"
AUTO_UPDATE_INTERVAL = 60  # Auto-update every 60 minutes
