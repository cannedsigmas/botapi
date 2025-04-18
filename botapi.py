import discord
from discord.ext import commands
import json
import os
import random

# Fetch the token from environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

GUILD_ID = '1362541680598716518'
CHANNEL_ID = '1362557856590856214'

file_path = r"C:\Users\canne\OneDrive\Documents\usernamedatabase\usernames_passwords.json"

# Set up intents, ensuring the message_content intent is enabled
intents = discord.Intents.default()
intents.message_content = True  # This enables the message content intent
bot = commands.Bot(command_prefix='/', intents=intents)

def read_json_data(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    return []

@bot.command(name='generate')
async def generate(ctx):
    data = read_json_data(file_path)

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
