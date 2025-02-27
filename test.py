# token: MTM0NDA4OTY5MDk1NzE1MjM4OA.G1KNDs.d3gUvq91Fx2fJYC87a-bVH6L-esqDJRK3AqIsw
# link: https://discord.com/oauth2/authorize?client_id=1344089690957152388&permissions=34816&integration_type=0&scope=bot

from slippi.slippi_api import SlippiRankedAPI

# Initialize the SlippiRankedAPI class
slippi_api = SlippiRankedAPI()

# Show slippi users data
slippi_user = slippi_api.get_player_ranked_data('fred#282', True)
print(slippi_user)