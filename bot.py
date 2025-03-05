import discord
from discord.ext import commands
import os

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')
    channel = discord.utils.get(bot.get_all_channels(), name="🚀-powerpicks")
    if channel:
        await channel.send("🚀 KP Wall Street Bot is now ONLINE!")

bot.run(TOKEN)
