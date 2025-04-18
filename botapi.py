import discord
from discord.ext import commands
import json
import random
import requests
import os

# Fetch the token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD_ID = '1362541680598716518'
CHANNEL_ID = '1362557856590856214'

# API endpoint URL for the Flask API (ngrok URL for Flask API)
api_url = "https://d439-71-210-135-30.ngrok-free.app/add_user"  # Replace with your actual ngrok URL

# Set up intents, ensuring the message_content intent is enabled
intents = discord.Intents.default()
intents.message_content = True  # This enables the message content intent
bot = commands.Bot(command_prefix='/', intents=intents)

# Function to send data to the Flask API (adding username and password)
def send_data_to_api(username, password):
    data = {'username': username, 'password': password}
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        print(f"✅ Successfully added {username} with password to the server.")
    else:
        print(f"❌ Failed to add {username} to the server. Status code: {response.status_code}")

@bot.command(name='generate')
async def generate(ctx):
    # Generate random username and password
    username = "user_" + str(random.randint(1000, 9999))
    password = "pass_" + str(random.randint(1000, 9999))

    # Send the generated username and password to the Flask API
    send_data_to_api(username, password)

    # Fetch usernames and passwords from the Flask API (optional)
    response = requests.get(f"https://d439-71-210-135-30.ngrok-free.app/get_usernames")
    if response.status_code == 200:
        data = response.json()
    else:
        data = []

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
