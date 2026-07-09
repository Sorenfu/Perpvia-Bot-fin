import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import asyncpg
from datetime import datetime, timedelta

load_dotenv()


# =========================
# Database
# =========================

db_pool = None


async def init_database():
    global db_pool

    db_pool = await asyncpg.create_pool(
        os.getenv("DATABASE_URL")
    )

    print("Database Connected")


# =========================
# Point Engine
# =========================

async def get_balance(user_id):

    async with db_pool.acquire() as conn:

        result = await conn.fetchrow(
            """
            SELECT points
            FROM users
            WHERE discord_id=$1
            """,
            user_id
        )

    if result:
        return result["points"]

    return 0



async def add_points(
    user_id,
    amount,
    source,
    reason
):

    async with db_pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO users
            (
                discord_id,
                points
            )
            VALUES
            (
                $1,
                $2
            )

            ON CONFLICT(discord_id)

            DO UPDATE SET

            points =
            users.points + $2

            """,
            user_id,
            amount
        )


        await conn.execute(
            """
            INSERT INTO point_transactions
            (
                user_id,
                amount,
                source,
                reason
            )

            VALUES
            (
                $1,
                $2,
                $3,
                $4
            )

            """,
            user_id,
            amount,
            source,
            reason
        )



# =========================
# Daily
# =========================


async def daily_checkin(user_id):

    async with db_pool.acquire() as conn:

        last = await conn.fetchrow(
            """
            SELECT created_at

            FROM daily_checkins

            WHERE user_id=$1

            ORDER BY created_at DESC

            LIMIT 1

            """,
            user_id
        )


    if last:

        if datetime.utcnow() - last["created_at"] < timedelta(hours=12):

            return False, "⏳ Daily cooldown active"


    await add_points(
        user_id,
        20,
        "daily",
        "Daily Check-in"
    )


    async with db_pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO daily_checkins
            (
                user_id,
                reward
            )

            VALUES
            (
                $1,
                $2
            )

            """,
            user_id,
            20
        )


    return True, "🎉 Daily +20 Points"



# =========================
# Discord Bot
# =========================


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

        await init_database()


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
            "Synced:",
            [
                x.name
                for x in synced
            ]
        )



bot = CommunityOS()



# =========================
# Commands
# =========================


@bot.tree.command(
    name="balance",
    description="View points balance"
)
async def balance(
    interaction: discord.Interaction
):

    points = await get_balance(
        interaction.user.id
    )


    await interaction.response.send_message(
        f"💎 Balance: {points} Points"
    )




@bot.tree.command(
    name="daily",
    description="Daily check in"
)
async def daily(
    interaction: discord.Interaction
):

    success, message = await daily_checkin(
        interaction.user.id
    )


    await interaction.response.send_message(
        message
    )




@bot.tree.command(
    name="shop",
    description="Open shop"
)
async def shop(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        "🛒 Shop system ready"
    )



# =========================
# Ready
# =========================


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
