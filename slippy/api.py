from slippi.slippi_api import SlippiRankedAPI

slippi_api = SlippiRankedAPI()

def fetch_player_data(slippi_code):
    """Fetches player data from Slippi API."""
    try:
        slippi_user = slippi_api.get_player_ranked_data(slippi_code, True)
        if not slippi_user or not hasattr(slippi_user, 'ranked_profile'):
            return None
        
        return {
            "username": slippi_user.display_name,
            "code": slippi_code,
            "elo": slippi_user.ranked_profile.rating_ordinal,
            "wins": slippi_user.ranked_profile.wins,
            "losses": slippi_user.ranked_profile.losses,
            "characters": ", ".join([char.character for char in slippi_user.ranked_profile.characters]) if hasattr(slippi_user.ranked_profile, 'characters') else ""
        }
    except Exception as e:
        print(f"❌ Error fetching player data: {e}")
        return None
