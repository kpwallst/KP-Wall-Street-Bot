import os
import requests
import pandas as pd
import discord
from discord.ext import commands

# Get the Alpha Vantage API key from environment variables
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

# Function to fetch stock data from Alpha Vantage
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" in data:
        time_series = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(time_series, orient="index")
        df = df.astype(float)
        return df
    else:
        return None

# Example: check for high volume breakouts
def find_high_volume_breakouts(stock_data):
    high_volume_threshold = stock_data['5. volume'].quantile(0.75)
    breakout_stocks = []

    for index, row in stock_data.iterrows():
        if row['5. volume'] > high_volume_threshold:
            breakout_stocks.append(index)
    
    return breakout_stocks

# Set up the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Command to fetch stock alerts
@bot.command()
async def stock_alert(ctx):
    symbols = ["AAPL", "MSFT", "GOOGL"]  # Example symbols
    alert_message = "The following stocks have high-volume breakouts today:\n"

    for symbol in symbols:
        stock_data = get_stock_data(symbol)
        if stock_data is not None:
            breakouts = find_high_volume_breakouts(stock_data)
            if breakouts:
                alert_message += f"{symbol}: {', '.join(breakouts)}\n"

    await ctx.send(alert_message)

# Run the bot
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
