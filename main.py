import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.guild:
        return

    owner_id = message.guild.owner_id

    # Verifica se mencionou o dono
    if message.mentions and any(user.id == owner_id for user in message.mentions):
        member = message.author

        # Tempo do mute (ex: 10 minutos)
        duration = timedelta(minutes=10)

        try:
            await member.timeout(duration, reason="Mencionou o dono do servidor")
            await message.reply("🚫 Não mencione o dono do servidor.")
        except discord.Forbidden:
            print("❌ Sem permissão para mutar")
        except Exception as e:
            print(e)

    await bot.process_commands(message)

bot.run(TOKEN)
