import json
import os
from config import DATA_FILE

def load_data():
    """Loads leaderboard and channel data from a JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"leaderboard": [], "channel_id": None, "last_leaderboard_message_id": None}

def save_data(leaderboard, leaderboard_channel_id, last_leaderboard_message_id):
    """Saves leaderboard and channel data to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump({
            "leaderboard": leaderboard,
            "channel_id": leaderboard_channel_id,
            "last_leaderboard_message_id": last_leaderboard_message_id
        }, f, indent=4)
