import discord
from discord.ext import commands
import requests
import random
import os

# Fetch the token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD_ID = '1362541680598716518'
CHANNEL_ID = '1362557856590856214'

# API endpoint URL (ngrok URL)
api_url = "https://fcdc-71-210-135-30.ngrok-free.app "  # Replace with your actual ngrok URL

# Set up intents, ensuring the message_content intent is enabled
intents = discord.Intents.default()
intents.message_content = True  # This enables the message content intent
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to fetch usernames from local API
def get_usernames_from_local_api():
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching usernames:", response.status_code)
        return []

@bot.command(name='generate')
async def generate(ctx):
    # Fetch usernames from the API
    data = get_usernames_from_local_api()

    if not data:
        await ctx.send("No available usernames and passwords found.")
        return

    selected_entry = random.choice(data)
    username = selected_entry['username']
    password = selected_entry['password']

    try:
        await ctx.author.send(f"Username:\n```{username}```")
        await ctx.author.send(f"Password:\n```{password}```")
        print(f"Sent {username} with password privately to {ctx.author.name}.")
    except discord.errors.Forbidden:
        await ctx.send("I can't DM you. Please make sure your DMs are open.")
        print(f"Could not send DM to {ctx.author.name}.")

bot.run(TOKEN)
