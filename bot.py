import discord
from discord.ext import commands
from datetime import timedelta
import os
import hashlib

token = os.getenv("DISCORD_TOKEN")

if not token:
    print("❌ TOKEN NÃO CHEGOU")
else:
    print("✅ TOKEN CHEGOU | hash:", hashlib.sha256(token.encode()).hexdigest())


TOKEN = "SEU_TOKEN_AQUI"

# ID da pessoa que NÃO pode ser mencionada
PROTECTED_USER_ID = 1331505963622076476

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Verifica se a pessoa protegida foi mencionada
    for mention in message.mentions:
        if mention.id == PROTECTED_USER_ID:
            try:
                # Timeout de 1 dia
                await message.author.timeout(
                    timedelta(days=1),
                    reason="Menção proibida"
                )

                await message.channel.send(
                    f"{message.author.mention} foi mutado por 1 dia por mencionar usuário proibido."
                )
            except discord.Forbidden:
                await message.channel.send(
                    "❌ Não tenho permissão para mutar este usuário."
                )
            except Exception as e:
                await message.channel.send(
                    f"Erro ao mutar usuário: {e}"
                )
            break

    await bot.process_commands(message)

bot.run(TOKEN)
