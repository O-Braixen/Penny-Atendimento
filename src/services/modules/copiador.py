import discord,os,json,asyncio
from discord.ext import commands
from discord import app_commands
from src.services.essential.respostas import Res
from dotenv import load_dotenv
from typing import Union







load_dotenv() #load .env da raiz
donoid = int(os.getenv("DONO_ID"))






class copiadora(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client











  @commands.Cog.listener()
  async def on_ready(self):
    print("📃 - Modúlo copiadora carregado.")













  @app_commands.command(name="copiador",description="💬⠂Copie todo o conteúdo de um chat para outro")
  @app_commands.describe(origem="canal de origem da copia.",destino="canal onde tudo será copiado.")
  async def copiador(self, interaction: discord.Interaction, origem: Union[discord.TextChannel, discord.Thread], destino: Union[discord.TextChannel, discord.Thread]):

    if interaction.user.id == donoid:
        if not origem or not destino:
            await interaction.response.send_message("Um ou ambos os canais não foram encontrados.", ephemeral=True, delete_after=15)
            return
         # Cria o webhook no canal de destino
        try:
          avatar = await self.client.user.avatar.read() if self.client.user.avatar else None
          webhook = await destino.create_webhook(name=self.client.user.name, avatar=avatar)
          await interaction.response.send_message("Iniciando copia por favor aguarde...", delete_after=15)
        except:
          await interaction.response.send_message("Erro no preparativo de copia...", delete_after=15)
          return

        try:
        # Acessa o histórico de todas as mensagens do canal de origem
            async for message in origem.history(limit=None, oldest_first=True):
                # Verifica anexos
                files = [await attachment.to_file() for attachment in message.attachments]
                # Verifica embeds
                embeds = message.embeds if message.embeds else []

                # Envia a mensagem no canal de destino com o webhook
                if message.content or files or embeds:
                    await webhook.send(
                        content=message.content if message.content else None,
                        username=message.author.display_name,
                        avatar_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url,
                        files=files,
                        embeds=embeds,
                        allowed_mentions=discord.AllowedMentions.none()
                    )
                    # Pausa para evitar limites da API
                    await asyncio.sleep(1)  # 1 segundo entre cada mensagem
        finally:
            # Remove o webhook após o uso
            await webhook.send(content=f"Eii {interaction.user.mention} terminei de copiar tudo do {origem.mention} para cá Kyuuuu")
            await webhook.delete()
    else:await interaction.response.send_message(Res.trad_nada( str="message_erro_onlyowner"),delete_after=20,ephemeral=True)












async def setup(client:commands.Bot) -> None:
  await client.add_cog(copiadora(client))
