from PIL import Image, ImageDraw, ImageFont

def generate_leaderboard_image(leaderboard):
    """Generates a visually appealing image displaying the Slippi leaderboard with modern style, mimicking Discord's dark mode."""

    rect_height = 150
    padding = 40
    row_padding = 35
    border_radius = 35

    # Dynamically adjust height based on the number of players
    num_players = len(leaderboard)
    total_height = 120 + (rect_height + row_padding) * num_players + 50  # 120px top margin, +50px bottom margin

    # Create an image
    img = Image.new("RGBA", (2400, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Load fonts
    leaderboard_font = ImageFont.truetype("arialbd.ttf", size=56)
    smaller_font = ImageFont.truetype("arialbd.ttf", size=28)
    slippi_code_font = ImageFont.truetype("arial.ttf", size=40)

    # Colors
    background_color = "#2C2F36"
    text_color = "#FFFFFF"
    muted_text_color = "#A1A1A1"

    # Draw each player's info inside a rounded rectangle
    y = 120
    for i, player in enumerate(leaderboard[:10]):
        rank = f"{i + 1}."
        player_name = player["username"]
        elo = round(player["elo"], 1)
        wins = player["wins"]
        losses = player["losses"]
        characters = player["characters"]
        slippi_code = player["code"].upper()

        # Define rectangle dimensions
        rect_x1 = 50
        rect_x2 = img.width - 50
        rect_y1 = y
        rect_y2 = y + rect_height

        # Draw rounded rectangle
        draw.rounded_rectangle([rect_x1, rect_y1, rect_x2, rect_y2], radius=border_radius, fill=background_color, outline="#4E5D6A", width=4)

        # Rank color logic
        rank_color = "#FFD700" if i == 0 else "#C0C0C0" if i == 1 else "#CD7F32" if i == 2 else "#FFFFFF"

        # Positioning text elements
        rank_position = (rect_x1 + padding, y + padding)
        player_position = (rect_x1 + 180, y + padding)

        left, top, right, bottom = draw.textbbox((0, 0), player_name, font=leaderboard_font)
        name_width = right - left
        slippi_code_position = (rect_x1 + 180 + name_width + 25, y + padding + 7)

        win_loss_position = (rect_x2 - 600, y + padding)
        elo_position = (rect_x2 - 250, y + padding)
        characters_position = (rect_x1 + 180, y + padding + 60)

        # Format win/loss text with `/` separator
        win_text = f"{wins}W"
        slash_text = " / "
        loss_text = f"{losses}L"

        # Draw text elements
        draw.text(rank_position, rank, font=leaderboard_font, fill=rank_color)
        draw.text(player_position, player_name, font=leaderboard_font, fill=text_color)
        draw.text(slippi_code_position, slippi_code, font=slippi_code_font, fill=muted_text_color)
        draw.text(elo_position, f"{elo}", font=leaderboard_font, fill=text_color)

        # Draw win/loss with correct colors and `/` separator
        win_x, win_y = win_loss_position
        draw.text((win_x, win_y), win_text, font=leaderboard_font, fill="#33CC33")  # High-saturation green

        slash_x = win_x + draw.textbbox((0, 0), win_text, font=leaderboard_font)[2]
        draw.text((slash_x, win_y), slash_text, font=leaderboard_font, fill="#D3D3D3")  # Light gray separator

        loss_x = slash_x + draw.textbbox((0, 0), slash_text, font=leaderboard_font)[2]
        draw.text((loss_x, win_y), loss_text, font=leaderboard_font, fill="#CC3333")  # High-saturation red

        # Draw characters below name
        draw.text(characters_position, f"Chars: {characters}", font=smaller_font, fill=muted_text_color)

        # Move to next row
        y += rect_height + row_padding

    # Save the image
    img.save("leaderboard.png", format="PNG")