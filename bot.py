import os
import discord
from discord.ext import commands
from datetime import timedelta

# ===== CONFIGURAÇÃO =====
PROTECTED_USER_ID = 1331505963622076476  # ID que NÃO pode ser mencionado
TIMEOUT_DURATION = timedelta(days=1)

# ===== TOKEN =====
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não encontrado nas variáveis de ambiente")

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message: discord.Message):
    # ignora bots
    if message.author.bot:
        return

    # verifica menção ao usuário protegido
    if any(user.id == PROTECTED_USER_ID for user in message.mentions):
        try:
            # apaga a mensagem
            await message.delete()

            # aplica timeout
            await message.author.timeout(
                TIMEOUT_DURATION,
                reason="Menção proibida"
            )
        except (discord.Forbidden, discord.HTTPException):
            pass  # silêncio absoluto

        return  # não processa mais nada

    await bot.process_commands(message)

# ===== START =====
bot.run(TOKEN)
