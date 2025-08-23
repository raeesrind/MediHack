# bot/main.py 

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.core.loader import load_cogs
import aiosqlite
import asyncio

# Import healthbot database module
from bot.database import database

load_dotenv(dotenv_path="config/.env")

intents = discord.Intents.all()

DATABASE = os.getenv("DATABASE", "medi.db")

# ---------------- Prefix from DB ----------------
async def get_prefix(bot, message):
    if not message.guild:
        return "?"

    guild_id = str(message.guild.id)
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT prefix FROM settings WHERE guild_id = ?", (guild_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return row[0]

    return "?"  # default


bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    help_command=None
)

bot.disabled_commands = {}

# ---------------- Checks ----------------
@bot.check
async def global_command_toggle_check(ctx):
    if not ctx.guild:
        return True
    guild_id = str(ctx.guild.id)
    command_name = ctx.command.name.lower() if ctx.command else None
    disabled = bot.disabled_commands.get(guild_id, [])
    return command_name not in disabled

# ---------------- Error Handling ----------------
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    embed = discord.Embed(
        title="⚠️ Error",
        description=str(error),
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

# ---------------- Ready Event ----------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    synced = await bot.tree.sync()
    print(f"🔄 Synced {len(synced)} global slash commands.")

    # Load disabled commands from DB
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT guild_id, disabled_commands FROM settings") as cursor:
            async for row in cursor:
                guild_id, disabled = row
                if disabled:
                    bot.disabled_commands[guild_id] = [cmd.strip().lower() for cmd in disabled.split(",")]
                else:
                    bot.disabled_commands[guild_id] = []

# ---------------- Main ----------------
async def main():
    # ✅ Initialize medi.db settings table
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            guild_id TEXT PRIMARY KEY,
            prefix TEXT DEFAULT '?',
            disabled_commands TEXT
        )
        """)
        await db.commit()

    # ✅ Initialize healthbot.db tables (users, hydration, BMI, stress, weight)
    await database.init_db()

    await load_cogs(bot)

    try:
        await bot.start(os.getenv("DISCORD_TOKEN"))
    finally:
        await bot.close()


def run_bot():
    asyncio.run(main())
