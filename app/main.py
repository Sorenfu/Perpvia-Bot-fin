import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from database.db import init_db
from core.points import PointEngine

load_dotenv()

class CommunityOS(discord.Client):
    def __init__(self):
        intents=discord.Intents.default()
        intents.members=True
        intents.message_content=True
        super().__init__(intents=intents)
        self.tree=app_commands.CommandTree(self)
        self.points=PointEngine()

    async def setup_hook(self):
        await init_db()
        guild=discord.Object(id=int(os.getenv('GUILD_ID')))
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print('Commands synced')

bot=CommunityOS()

@bot.tree.command(name='balance',description='View points')
async def balance(interaction):
    value=await bot.points.balance(interaction.user.id)
    await interaction.response.send_message(f'💎 Balance: {value} Points')

@bot.tree.command(name='daily',description='Daily checkin')
async def daily(interaction):
    await interaction.response.send_message('Daily integration ready')

@bot.tree.command(name='shop',description='Open shop')
async def shop(interaction):
    await interaction.response.send_message('Shop integration ready')

@bot.event
async def on_ready():
    print(f'Community OS Ready: {bot.user}')

bot.run(os.getenv('DISCORD_TOKEN'))
