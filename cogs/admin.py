import discord,os,asyncio
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from cogs.onwer import getdonoid,getmensagemerro

#coleta as informações de outro .py
donoid = getdonoid()
mensagemerro = getmensagemerro()

erropermissão = "❌┃ Kyuuu... Parece que eu não tenho permissão de fazer isso."
errobanir = "❌┃ Kyuuu... Parece que eu não tenho permissão de banir ou esse membro já foi banido."

#inicio dessa classe
class admin(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  #faz esse cara ser ouvido no main
  @commands.Cog.listener()
  async def on_ready(self):
    print("Cog admin carregado.")
    

  #GRUPO ADMINISTRADOR - grupo de comandos
  admin=app_commands.Group(name="admin",description="Comandos de controle do bot.")

   #COMANDO BANIR - dentro do grupo admin
  @admin.command(name="banir",description='💼⠂Banir um membro do servidor')
  @app_commands.describe(membro="Qual membro será banido?",razão="Qual a razão do banimento?")
  @commands.has_permissions(ban_members=True)
  async def ban(self,interaction: discord.Interaction, membro: discord.Member, razão: str):
    print (f"Usuario: {interaction.user.name} usou banir em: {membro}")
    await interaction.response.defer()
    try:
      if interaction.permissions.ban_members:
        resposta = discord.Embed(
            colour=discord.Color.red(),
            title="🦊┃Banido",
            description=f"Membro: {membro}\nRazão: {razão}"
        )
        await membro.ban(reason=razão)
        await interaction.followup.send(embed=resposta)
      else: await interaction.followup.send(mensagemerro,ephemeral=True)
    except discord.Forbidden:
      await interaction.response.send_message(errobanir, ephemeral=True)
  

#COMANDO DESBANIR - dentro do grupo admin
  @admin.command(name="desbanir",description='💼⠂Desbanir um membro do servidor')
  @app_commands.describe(membro="Qual membro será desbanido?")
  @commands.has_permissions(ban_members=True)
  async def unban(self,interaction: discord.Interaction, membro:str):
    print (f"Usuario: {interaction.user.name} usou desbanir em: {membro}")
    try:
      if interaction.permissions.ban_members:
        membro = int(membro)
        user = await self.client.fetch_user(membro)
        await interaction.guild.unban(user)
        resposta = discord.Embed(
            colour=discord.Color.yellow(),
            title="🦊┃Desbanido",
            description=f"Membro: {membro}"
        )
        await interaction.response.send_message(embed=resposta)
        return
      else: await interaction.followup.send(mensagemerro,ephemeral=True)
    except Exception:
      await interaction.response.send_message(errobanir, ephemeral=True)
  

    #COMANDO KICK - dentro do grupo admin
  @admin.command(name="kick", description='💼⠂Expulsar um membro do servidor')
  @app_commands.describe(membro="Qual membro será expulso?", razão="Qual a razão da expulsão?")
  @commands.has_permissions(kick_members=True)
  async def kick(self, interaction: discord.Interaction, membro: discord.Member, razão: str):
    print(f"Usuario: {interaction.user.name} usou kick em: {membro}")
    await interaction.response.defer()
    try:
        if interaction.permissions.kick_members:
            resposta = discord.Embed(
                colour=discord.Color.orange(),
                title="🦊┃Expulso",
                description=f"Membro: {membro}\nRazão: {razão}"
            )
            await membro.kick(reason=razão)
            await interaction.followup.send(embed=resposta)
        else:
            await interaction.followup.send(mensagemerro, ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(erropermissão, ephemeral=True)

    

  #GRUPO CHAT 
  chat=app_commands.Group(name="chat",description="Comandos de chat do bot.")

  #COMANDO DELETE CHAT
  @chat.command(name="deletar",description='🗨️⠂Deleta um chat existente')
  async def deletechat(self,interaction: discord.Interaction):
    print (f"Usuario: {interaction.user.name} usou deletar canal em: {interaction.channel.name}")
    if interaction.permissions.manage_channels:
        await interaction.response.send_message("✅┃bye bye chat...")
        await asyncio.sleep(2.0)
        await interaction.channel.delete()
    else: await interaction.response.send_message(mensagemerro,ephemeral=True)


  #COMANDO PRUNE CHAT
  @chat.command(name="limpar",description='🗨️⠂Limpa as mensagems de um canal')
  @app_commands.describe(quantidade="informe a quantidade de mensagens para deletar")
  async def prunechat(self,interaction: discord.Interaction, quantidade:int):
    print (f"Usuario: {interaction.user.name} usou limpar chat em: {interaction.channel.name}")
    if interaction.permissions.manage_channels:
        await interaction.response.send_message("<:stick:969703475720126464> - Limpando o chat...",ephemeral=True)
        await interaction.channel.purge(limit=quantidade)
    else: await interaction.response.send_message(mensagemerro,ephemeral=True)


 #COMANDO CRIAR CHAT
  @chat.command(name="criar",description='🗨️⠂Crie um novo chat')
  @app_commands.describe(nome="informe um nome para o chat")
  async def createchat(self,interaction: discord.Interaction, nome:str,categoria:discord.CategoryChannel=None):
    print (f"Usuario: {interaction.user.name} usou limpar chat em: {interaction.channel.name}")
    if interaction.permissions.manage_channels:
        if categoria is None:
          novo_canal = await interaction.guild.create_text_channel(nome)
        else: novo_canal = await interaction.guild.create_text_channel(nome,category=categoria)
        await interaction.response.send_message(f"<:stick:969703475720126464> - Criei o canal de texto {novo_canal.mention} para você.",ephemeral=True)
    else: await interaction.response.send_message(mensagemerro,ephemeral=True)


#COMANDO INFO CHAT
  @chat.command(name="info",description='🗨️⠂Informações sobre um chat')
  @app_commands.describe(chat="informe um chat para consultar")
  async def infochat(self,interaction: discord.Interaction, chat: discord.TextChannel=None):
    print (f"Usuario: {interaction.user.name} usou chat info")
    if chat is None:
        chat = interaction.channel
    topico = chat.topic or "Nenhum tópico definido."
    if chat.nsfw is True:
       nsfw = "Sim"
    else: 
       nsfw = "Não"
    if chat.slowmode_delay == 0:
       slow = "Desativado"
    else: 
       slow = f"Ativado em {chat.slowmode_delay}s"
    resposta = discord.Embed(
      colour=discord.Color.yellow(),
      title=f"🦊┃Informações do Chat", 
      description=f"```{topico}```"
    )
    resposta.add_field(name=":small_blue_diamond:⠂Menção", value=f"```<#{chat.id}>```", inline=True)
    resposta.add_field(name="⚙️⠂Tipo", value=f"```Chat de Texto```", inline=True)    
    resposta.add_field(name="🔞⠂NSFW", value=f"```{nsfw}```", inline=True)
    resposta.add_field(name="⌛⠂Modo Lento", value=f"```{slow}```", inline=True)    
    resposta.add_field(name="🪪⠂Nome", value=f"```{chat.name}```", inline=True)    
    resposta.add_field(name="📅⠂Data Criação", value=f"```{datetime.strftime(chat.created_at, '%d/%m/%Y')}```", inline=True)    
    await interaction.response.send_message(embed=resposta)


  #GRUPO CANAL 
  canal=app_commands.Group(name="canal",description="Comandos de canais do bot.")

  #COMANDO DELETE CANAL
  @canal.command(name="deletar",description='🗨️⠂Deleta um canal existente')
  async def deletechannel(self,interaction: discord.Interaction,canal: discord.VoiceChannel):
    print (f"Usuario: {interaction.user.name} usou deletar canal em: {interaction.channel.name}")
    if interaction.permissions.manage_channels:
        await interaction.response.send_message("✅┃bye bye canal...")
        await canal.delete()
    else: await interaction.response.send_message(mensagemerro,ephemeral=True)

  #COMANDO CRIAR CANAL
  @canal.command(name="criar",description='🗨️⠂Crie um novo canal')
  @app_commands.describe(nome="informe um nome para o chat")
  async def createchannel(self,interaction: discord.Interaction, nome:str,categoria:discord.CategoryChannel=None):
    print (f"Usuario: {interaction.user.name} usou limpar chat em: {interaction.channel.name}")
    if interaction.permissions.manage_channels:
        if categoria is None:
          novo_canal = await interaction.guild.create_voice_channel(nome)
        else: novo_canal = await interaction.guild.create_voice_channel(nome,category=categoria)
        await interaction.response.send_message(f"<:stick:969703475720126464> - Criei o canal de texto {novo_canal.mention} para você.",ephemeral=True)
    else: await interaction.response.send_message(mensagemerro,ephemeral=True)

#COMANDO INFO CANAL
  @canal.command(name="info",description='🗨️⠂Informações sobre um canal')
  @app_commands.describe(canal="informe um chat para consultar")
  async def infochat(self,interaction: discord.Interaction, canal: discord.VoiceChannel):
    print (f"Usuario: {interaction.user.name} usou canal info")
    if canal is None:
        canal = interaction.channel
    if canal.nsfw is True:
       nsfw = "Sim"
    else: nsfw = "Não"

    if canal.user_limit == 0:
       canallimite = "Ilimitado"
    else: canallimite = canal.user_limit
    resposta = discord.Embed(
      colour=discord.Color.yellow(),
      title=f"🦊┃Informações de {canal.name}", 
    )
    resposta.add_field(name=":small_blue_diamond:⠂Menção", value=f"```<#{canal.id}>```", inline=True)
    resposta.add_field(name="⚙️⠂Tipo", value=f"```Chat de Voz```", inline=True)    
    resposta.add_field(name="🔞⠂NSFW", value=f"```{nsfw}```", inline=True)
    resposta.add_field(name="🎙⠂Taxa de Bits", value=f"```{round(canal.bitrate / 1000)}kbps```", inline=True)    
    resposta.add_field(name=":busts_in_silhouette:⠂Membros", value=f"```{canallimite}```", inline=True)    
    resposta.add_field(name="📅⠂Data Criação", value=f"```{datetime.strftime(canal.created_at, '%d/%m/%Y')}```", inline=True)    
    await interaction.response.send_message(embed=resposta)

  #GRUPO CARGO 
  cargo=app_commands.Group(name="cargo",description="Comandos de cargo do bot.")

  #COMANDO ADD ROLE
  @cargo.command(name="adicionar",description='🔑⠂Adiciona um cargo a um membro')
  @app_commands.describe(membro="informe um membro",cargo="qual cargo deseja adicionar ao membro?")
  @commands.has_permissions(manage_roles=True)
  async def roleadd(self,interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role):
    print (f"Usuario: {interaction.user.name} usou add cargo")
    try:
      if interaction.permissions.manage_roles:
        resposta = discord.Embed(
          colour=discord.Color.yellow(),
          title="🦊┃Cargo Adicionado",
          description=f"Membro: {membro.mention}\nCargo: {cargo}"
        )
        await membro.add_roles(cargo)
        await interaction.response.send_message(embed=resposta)
      else: await interaction.response.send_message(mensagemerro,ephemeral=True)
    except discord.Forbidden:
      await interaction.response.send_message(erropermissão, ephemeral=True)
      
  #COMANDO REM ROLE
  @cargo.command(name="remover",description='🔑⠂Remove um cargo de um membro')
  @app_commands.describe(membro="informe um membro",cargo="qual cargo deseja remover do membro?")
  @commands.has_permissions(manage_roles=True)
  async def rolerem(self,interaction: discord.Interaction, membro: discord.Member, cargo: discord.Role):
    print (f"Usuario: {interaction.user.name} usou rem cargo")
    try:
      if interaction.permissions.manage_roles:
        resposta = discord.Embed(
          colour=discord.Color.yellow(),
          title="🦊┃Cargo Removido",
          description=f"Membro: {membro.mention}\nCargo: {cargo}"
        )
        await membro.remove_roles(cargo)
        await interaction.response.send_message(embed=resposta)
      else: await interaction.response.send_message(mensagemerro,ephemeral=True)
    except discord.Forbidden:
      await interaction.response.send_message(erropermissão, ephemeral=True)
     
    #COMANDO SWITCH ROLE
  @cargo.command(name="trocar",description='🔑⠂Troca o cargo a um membro')
  @app_commands.describe(membro="informe um membro",retirar="qual cargo deseja remover do membro?",colocar="qual cargo deseja adicionar ao membro?")
  @commands.has_permissions(manage_roles=True)
  async def rolecharge(self,interaction: discord.Interaction, membro: discord.Member, retirar: discord.Role, colocar: discord.Role):
    print (f"Usuario: {interaction.user.name} usou trocar cargo")
    try:
      if interaction.permissions.manage_roles:
        resposta = discord.Embed(
          colour=discord.Color.yellow(),
          title="🦊┃Cargo Trocado",
          description=f"Membro: {membro.mention}\nCargo: {retirar.mention} 🔁 {colocar.mention}"
        )
        await membro.remove_roles(retirar)
        await membro.add_roles(colocar)
        await interaction.response.send_message(embed=resposta)
      else: await interaction.response.send_message(mensagemerro,ephemeral=True)
    except discord.Forbidden:
      await interaction.response.send_message(erropermissão, ephemeral=True)
  
  #COMANDO CARGO INFO
  @cargo.command(name="info",description='🔑⠂Verifica as informações de um cargo')
  @app_commands.describe(cargo="selecione um cargo")
  async def roleinfo(self,interaction: discord.Interaction, cargo: discord.Role):
    resposta = discord.Embed( 
        colour=cargo.color,
        description=f"**📂┃Informações de {cargo.name}**"
    )
    if cargo.mentionable is True:
        mençãocargo = "✅"
    else: mençãocargo = "❌"
    if cargo.hoist is True:
        cargoseparado = "✅"
    else: cargoseparado = "❌"
    resposta.set_thumbnail(url=cargo.icon)
    resposta.add_field(name="🪪⠂Nome", value=f"```{cargo.name}```", inline=True)
    resposta.add_field(name="🆔⠂ID", value=f"```{cargo.id}```", inline=True)
    resposta.add_field(name="🦊⠂menção", value=cargo.mention, inline=True)
    resposta.add_field(name=f"⚙️⠂Especificações", value=f"```Mensionável: {mençãocargo}\nSeparado: {cargoseparado}```", inline=True)
    resposta.add_field(name="📅⠂Criado em", value=f"```{datetime.strftime(cargo.created_at, '%d/%m/%Y')}```", inline=True)
    members_with_role = len(cargo.members)
    resposta.add_field(name=f"💼⠂Membros", value=f"```{members_with_role} Usuários```", inline=True)
    await interaction.response.send_message(embed=resposta)

async def setup(client:commands.Bot) -> None:
  await client.add_cog(admin(client))