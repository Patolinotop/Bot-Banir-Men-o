import discord
from discord.ext import commands
from datetime import timedelta
import os
import hashlib

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN não encontrado")
else:
    print("✅ TOKEN CHEGOU | hash:", hashlib.sha256(TOKEN.encode()).hexdigest())

PROTECTED_USER_ID = 1331505963622076476

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if any(u.id == PROTECTED_USER_ID for u in message.mentions):
        await message.author.timeout(
            timedelta(days=1),
            reason="Menção proibida"
        )
        await message.channel.send(
            f"🔇 {message.author.mention} mutado por 1 dia."
        )

    await bot.process_commands(message)

bot.run(TOKEN)
