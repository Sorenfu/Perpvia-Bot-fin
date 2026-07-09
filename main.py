import os
import discord
from discord import app_commands
from dotenv import load_dotenv

from database.db import init_db
from commands.loader import load_commands
from events.loader import load_events


load_dotenv()


class CommunityOS(discord.Client):

    def __init__(self):

        intents = discord.Intents.default()

        intents.members = True

        intents.message_content = True


        super().__init__(
            intents=intents
        )


        self.tree = app_commands.CommandTree(self)



    async def setup_hook(self):

        print("Community OS Starting...")


        # Database

        await init_db()


        print(
            "Database Connected"
        )


        # Load Commands

        load_commands(
            self.tree
        )


        print(
            "Commands Loaded"
        )


        # Load Events

        load_events(
            self
        )


        print(
            "Events Loaded"
        )


        # Discord Guild Sync

        guild = discord.Object(
            id=int(
                os.getenv(
                    "GUILD_ID"
                )
            )
        )


        self.tree.copy_global_to(
            guild=guild
        )


        synced = await self.tree.sync(
            guild=guild
        )


        print(
            "Synced Commands:",
            [
                cmd.name
                for cmd in synced
            ]
        )



bot = CommunityOS()



@bot.event
async def on_ready():

    print(
        f"Community OS Ready: {bot.user}"
    )



bot.run(
    os.getenv(
        "DISCORD_TOKEN"
    )
)
