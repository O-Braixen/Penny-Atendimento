import discord,os,asyncio,time,json
from discord.ext import commands
from discord import app_commands
from src.services.essential.respostas import Res
from dotenv import load_dotenv


# Substitua com o ID do canal específico que você deseja monitorar
load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) #load .env da raiz
ID_SERVIDOR_BH = int(os.getenv("id_servidor_bh"))
CARGO_REVIVER_CHAT= int(os.getenv("id_cargo_reviverchat"))









class reviverchat(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client








  @commands.Cog.listener()
  async def on_ready(self):
    print("🦊 - Modúlo reviverchat BH carregado.")



     # Pegando a comunidade (servidor) pelo ID
    guild = self.client.get_guild(ID_SERVIDOR_BH)
    if guild is None:
      print("⚠️ - Servidor não encontrado! Verifique a ID.")
      return


        # Pegando o cargo pelo ID
    cargo = guild.get_role(CARGO_REVIVER_CHAT)
    if cargo:
      await cargo.edit(mentionable=True)  # Tornando o cargo mencionável
      print(f"🔄 - Cargo '{cargo.name}' reativado como mencionável.")
    else:
      print("⚠️ - Cargo não encontrado! Verifique a ID.")











  
  #Fazer coisas aqui nessa parte, lembrar de respeitar a organização

  @commands.Cog.listener()
  async def on_message(self,message):
    if message.author == self.client.user or message.author.bot:
            return
    elif f"<@&{CARGO_REVIVER_CHAT}>" in message.content and message.author != self.client.user:
        cargo = discord.utils.get(message.guild.roles, name="🔥 Reviver Chat")
        print(cargo.id)
        msg = await message.reply(Res.trad_nada(str='message_revier_chat'))
        await cargo.edit(mentionable=False)
        print("ping reviver chat desativado")
        await asyncio.sleep(35)
        await msg.delete()
        await asyncio.sleep(7165)
        await cargo.edit(mentionable=True)
        print("ping reviver chat reativado")
    else:
      return
  








async def setup(client:commands.Bot) -> None:
  await client.add_cog(reviverchat(client))