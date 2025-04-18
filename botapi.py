import discord
from discord.ext import commands
import json
import os
import random

# Use environment variables for the bot token
TOKEN = os.getenv('DISCORD_TOKEN')  # Get the token from the environment variable

# These values can also be set via environment variables if desired
GUILD_ID = '1362541680598716518'
CHANNEL_ID = '1362557856590856214'

# Path to the JSON file (this path will need to be adjusted if deploying in a server environment)
file_path = r"C:\Users\canne\OneDrive\Documents\usernamedatabase\usernames_passwords.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

def read_json_data(file_path):
    """Function to read the JSON file and return the data."""
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    return []

@bot.command(name='generate')
async def generate(ctx):
    """Command to generate a username and password and send it to the user."""
    data = read_json_data(file_path)

    if not data:
        await ctx.send("No available usernames and passwords found.")
        return

    selected_entry = random.choice(data)
    username = selected_entry['username']
    password = selected_entry['password']

    try:
        # Attempt to send the username and password to the user's DM
        await ctx.author.send(f"Username:\n```{username}```")
        await ctx.author.send(f"Password:\n```{password}```")
        print(f"Sent {username} with password privately to {ctx.author.name}.")
    except discord.errors.Forbidden:
        await ctx.send("I can't DM you. Please make sure your DMs are open.")
        print(f"Could not send DM to {ctx.author.name}.")

# Run the bot using the token stored in the environment variable
bot.run(TOKEN)
