import discord,os,random,asyncio
from discord.ext import commands
from discord import app_commands,utils
from datetime import datetime


afklist = [] #Lista de usuarios afk vazia para ser usada depois
      #FUNCÔES AQUII EM BAIXO

#FUNÇÂO USUARIO INFO
async def buscaruser(interaction,membro,menu):
  print (f"Usuario: {interaction.user.name} usou comando usuario")
  if membro == None:
    membro = interaction.user
  resposta = discord.Embed(
    colour=discord.Color.yellow(),
    description=f"**🗄️┃Informações de {membro.name}**"
  )
  resposta.set_thumbnail(url=membro.avatar.url)
  resposta.add_field(name="🪪⠂Nome", value=f"```{membro.name}#{membro.discriminator}```", inline=True)
  resposta.add_field(name="🆔⠂ID", value=f"```{membro.id}```", inline=True)
  resposta.add_field(name="🦊⠂menção", value=membro.mention, inline=True)
  resposta.add_field(name="📅⠂Entrou no servidor", value=f"```{datetime.strftime(membro.joined_at, '%d/%m/%Y às %H:%M:%S')}```", inline=True)
  resposta.add_field(name="👋⠂Entrou no discord", value=f"```{datetime.strftime(membro.created_at, '%d/%m/%Y às %H:%M:%S')}```", inline=True)
  if len(membro.roles) == 1:
    resposta.add_field(name=f"💼⠂Cargos ({len(membro.roles) - 1})", value="```🦊⠂Sem cargos```", inline=False)
  else:
     roles_list = [role.mention for role in membro.roles if role.name != '@everyone']
     if len(roles_list) > 5:
        roles_list = roles_list[:5]  # Limita a lista aos primeiros 5 cargos
        roles_list.append("...")  # Adiciona "..." para indicar que há mais cargos
        resposta.add_field(name=f"💼⠂Cargos ({len(membro.roles) - 1})", value='\n • '.join(roles_list), inline=False)
     else:resposta.add_field(name=f"💼⠂Cargos ({len(membro.roles) - 1})", value='\n • '.join([role.mention for role in membro.roles if role.name != '@everSyone']), inline=False)
  if menu is True: #isso verifica se o comando veio do menu se sim ele manda como ephemeral
     await interaction.response.send_message(embed=resposta,ephemeral=True)
  else: await interaction.response.send_message(embed=resposta)


#Função USUARIO AVATAR
async def buscaravatar(interaction,membro,menu):
  print (f"Usuario: {interaction.user.name} usou avatar")
  if membro == None:
    membro = interaction.user
  resposta = discord.Embed(
    title="🦊┃Avatar de Usuário",
    description=f"Aqui está o avatar do membro: {membro.name}",
    colour=discord.Color.yellow()
  )
  resposta.set_image(url=f"{membro.avatar}")
  view = discord.ui.View()
  item = discord.ui.Button(style=discord.ButtonStyle.blurple,label="abrir em navegador",url=f"{membro.avatar.url}")
  view.add_item(item=item)
  if menu is True: #isso verifica se o comando veio do menu se sim ele manda como ephemeral
     await interaction.response.send_message(embed=resposta,view=view,ephemeral=True)
  else: await interaction.response.send_message(embed=resposta,view=view)


#FUNÇÂO USUARIO ABRAÇAR
async def funcaoabracarusuario(interaction,membro):
  print (f"Usuario: {interaction.user.name} usou avatar")
  #o imagem é uma lista de links de imagens que serão sorteados e um será enviado
  imagem = ["https://33.media.tumblr.com/8ac1eaeaa670c65b7dbb9ceff34e4d8b/tumblr_ntdyqagJ101r8sc3ro1_r1_500.gif","https://media.tenor.com/AyIx-RCO4aQAAAAC/pokemon-hug.gif"]
  resposta = discord.Embed(
    description=f"🦊┃{interaction.user.mention} abraçou {membro.mention}!",
    colour=discord.Color.yellow()
  )
  resposta.set_image(url=f"{random.choice(imagem)}")
  await interaction.response.send_message(embed=resposta)
  


#INICIO DA CLASSE
class misc(commands.Cog):
  def __init__(self, client: commands.Bot) -> None:
        self.client = client
        #Carrega os menu e adiciona eles
        self.menu_useravatar = app_commands.ContextMenu(name="Usuario Avatar",callback=self.useravatarmenu)
        self.menu_userinfo = app_commands.ContextMenu(name="Usuario Info",callback=self.userinfomenu)
        self.menu_userbanner = app_commands.ContextMenu(name="Usuario Banner",callback=self.userbannermenu)
        self.menu_userabraco = app_commands.ContextMenu(name="Usuario Abraço",callback=self.userabracomenu)
        self.client.tree.add_command(self.menu_useravatar)
        self.client.tree.add_command(self.menu_userinfo)
        self.client.tree.add_command(self.menu_userbanner)
        self.client.tree.add_command(self.menu_userabraco)

  @commands.Cog.listener()
  async def on_ready(self):
    print("Cog Misc carregado.")

  @commands.Cog.listener()
  #esse on_messagem é responsavel pelo sistema de avisos /bump e do afk dos usuarios
  async def on_message(self,message):
    #verifica todos os usuarios da lista de afk
    for i in range(len(afklist)):
      if (f"<@{afklist[i]}>" in message.content) and (not message.author.bot):
        msgenviada = await message.channel.send(f"<:BraixSleep:988776304587440148>┃ eiii {message.author.mention} quem você marcou **está afk** no momento pelo motivo: `{afklist[i+1]}`")
        await asyncio.sleep(15.0)
        await msgenviada.delete()
        return None
      break
    
    # essa parte aqui verifica se o bot disboard manda a confirmação de bump dele e essa parte pega e ativa o lembrete
    if message.author.bot and message.embeds:
      if message.embeds and message.embeds[0].description and "Bump done!" in message.embeds[0].description and message.author and message.author.id == 302050872383242240:
        await message.add_reaction('👍')
        #a baixo é a mensagem de confirmação de ativação
        msgenviada = await message.channel.send("<:BraixHappy2:988776437790158918>┃ Uhull alguem deu bump ~kyuu!\nIrei tentar te avisar do proximo bump <:BraixSussy:984628386947289089>")
        cargo = discord.utils.get(message.guild.roles, name="👍 Bump") # aqui eu verifico se no servidor tem o cargo @👍 Bump
        await asyncio.sleep(15)
        await msgenviada.delete()
        await asyncio.sleep(7190)
        print(f"mandando lembrete de bump para {message.guild.name}!")
        if cargo is not None:
          #se tem cargo bump roda isso, caso contrario roda oque ta no else
          await message.channel.send(f"<a:patpatBraixen:1112706846042628126>┃ Eaiii <@&{cargo.id}> já podem dar </bump:947088344167366698> novamente!")
        else: 
          await message.channel.send(f"<a:patpatBraixen:1112706846042628126>┃ Eaiii já podem dar </bump:947088344167366698> novamente! \n<:UlikeKissingBraixens:1108359276126285867> ┃ **Dica de raposa:** Crie em sua comunidade o cargo chamado `👍 Bump` para que eu possa notificar nele os proximos bumps ~kyu.")


  @commands.Cog.listener()
  #verifica todos os usuarios que digitam, se ele estiver na afklist ele desativa o afk automaticamente
  async def on_typing(self, channel, user, when):
    if user.id in afklist:
      i = afklist.index(user.id)
      afklist.remove(afklist[i+1])
      afklist.remove(user.id)
      msgenviada = await channel.send(f"<:BraixTongue:905841511323828265>┃ {user.mention} seu afk foi desativado!!!")
      print(f"{user.mention} saiu do afk")
      await asyncio.sleep(15.0)
      await msgenviada.delete()


  #Remove os menu se necessario - deixa isso aqui é importante ter
  async def cog_unload(self) -> None:
        self.client.tree.remove_command(self.menu_useravatar, type=self.menu_useravatar.type)
        self.client.tree.remove_command(self.menu_userinfo, type=self.menu_userinfo.type)
        self.client.tree.remove_command(self.menu_userbanner, type=self.menu_userbanner.type)


#GRUPO USUARIOS 
  usuario=app_commands.Group(name="usuario",description="Comandos de usuarios do bot.")

#COMANDO USUARIO AVATAR MENU
  async def useravatarmenu(self,interaction: discord.Interaction, membro: discord.Member):
    menu = True
    await buscaravatar(interaction,membro,menu)# chama a função lá em cima

#COMANDO USUARIO AVATAR SLASH
  @usuario.command(name="avatar",description='👤⠂Exibe o avatar de um membro')
  @app_commands.describe(membro="informe um membro")
  async def useravatar(self,interaction: discord.Integration,membro: discord.Member=None):
    menu = False
    await buscaravatar(interaction,membro,menu)# chama a função lá em cima

#COMANDO USUARIO INFO MENU
  async def userinfomenu(self,interaction: discord.Interaction, membro: discord.Member):
    menu = True
    await buscaruser(interaction,membro,menu)# chama a função lá em cima

#COMANDO USUARIO INFO SLASH
  @usuario.command(name="info",description='👤⠂Verifica as informações de um membro')
  @app_commands.describe(membro="informe um membro")
  async def userinfo(self,interaction: discord.Integration,membro: discord.Member=None):
    menu = False
    await buscaruser(interaction,membro,menu)# chama a função lá em cima
 
#COMANDO USUARIO ABRAÇO MENU
  async def userabracomenu(self,interaction: discord.Interaction, membro: discord.Member):
    await funcaoabracarusuario(interaction,membro) # chama a função lá em cima

#COMANDO USUARIO ABRAÇO SLASH
  @usuario.command(name="abraçar",description='👤⠂Abraçe um membro')
  @app_commands.describe(membro="informe um membro")
  async def userabraco(self,interaction: discord.Integration,membro: discord.Member):
    await funcaoabracarusuario(interaction,membro) # chama a função lá em cima

#COMANDO USUARIO BANNER MENU
  async def userbannermenu(self,interaction: discord.Interaction, membro: discord.Member=None):
    print (f"Usuario: {interaction.user.name} usou banner")
    if membro == None:
        membro = interaction.user
    membro = await self.client.fetch_user(membro.id)
    if membro.banner:
      resposta = discord.Embed(
        title=f"🦊┃Banner de {membro.name}",
        colour=discord.Color.yellow()
      )
      resposta.set_image(url=f"{membro.banner.url}")
      view = discord.ui.View()
      item = discord.ui.Button(style=discord.ButtonStyle.blurple,label="abrir em navegador",url=f"{membro.banner.url}")
      view.add_item(item=item)
      await interaction.response.send_message(ephemeral=True,embed=resposta,view=view)
    else:await interaction.response.send_message(f"<:BraixBlank:969396003436380200> - Parece que o {membro.mention} não possui um banner kyu~~.", ephemeral=True)


#COMANDO USUARIO BANNER SLASH
  @usuario.command(name="banner",description='👤⠂Exibe o banner de um membro')
  @app_commands.describe(membro="informe um membro")
  async def userbanner(self,interaction: discord.Interaction, membro: discord.Member=None):
    print (f"Usuario: {interaction.user.name} usou banner")
    if membro == None:
        membro = interaction.user
    membro = await self.client.fetch_user(membro.id)
    if membro.banner:
      resposta = discord.Embed(
        title=f"🦊┃Banner de {membro.name}",
        colour=discord.Color.yellow()
      )
      resposta.set_image(url=f"{membro.banner.url}")
      view = discord.ui.View()
      item = discord.ui.Button(style=discord.ButtonStyle.blurple,label="abrir em navegador",url=f"{membro.banner.url}")
      view.add_item(item=item)
      await interaction.response.send_message(embed=resposta,view=view)
    else:await interaction.response.send_message(f"<:BraixBlank:969396003436380200> - Parece que o {membro.mention} não possui um banner kyu~~.", ephemeral=True)

#COMANDO USUARIO ABRAÇO SLASH
  @usuario.command(name="atacar",description='👤⠂Ataque um membro')
  @app_commands.describe(membro="informe um alvo")
  async def userabraco(self,interaction: discord.Integration,membro: discord.Member):
    print (f"Usuario: {interaction.user.name} usou atacar")
    resposta = discord.Embed(
      description=f"🔥┃{interaction.user.mention} tacou fogo em {membro.mention}!",
      colour=discord.Color.yellow()
    )
    resposta.set_image(url=f"https://64.media.tumblr.com/dcfc44e780bdf2427abdc852f960e981/tumblr_oktry4hti91tgjlm2o1_500.gif")
    await interaction.response.send_message(embed=resposta)
  
#COMANDO USUARIO ABRAÇO SLASH
  @usuario.command(name="carinho",description='👤⠂Faça carinho em um membro')
  @app_commands.describe(membro="informe um membro")
  async def userabraco(self,interaction: discord.Integration,membro: discord.Member):
    print (f"Usuario: {interaction.user.name} usou carinho")
    resposta = discord.Embed(
      description=f"🦊┃{interaction.user.mention} fez carinho em {membro.mention}!",
      colour=discord.Color.yellow()
    )
    resposta.set_image(url=f"https://i.makeagif.com/media/6-13-2015/5aAShu.gif")
    await interaction.response.send_message(embed=resposta)

#COMANDO USUARIO CAFUNÉ SLASH
  @usuario.command(name="cafuné",description='👤⠂Faça cafuné em um membro')
  @app_commands.describe(membro="informe um membro")
  async def userabraco(self,interaction: discord.Integration,membro: discord.Member):
    print (f"Usuario: {interaction.user.name} usou cafuné")
    resposta = discord.Embed(
      description=f"🦊┃{interaction.user.mention} fez cafuné em {membro.mention}!",
      colour=discord.Color.yellow()
    )
    resposta.set_image(url=f"https://cdn.discordapp.com/attachments/1067789510097768528/1139147429367791696/Braixen_carinho.gif")
    await interaction.response.send_message(embed=resposta)


#COMANDO USUARIO AFK
  @usuario.command(name="afk",description='👤⠂fique afk')
  @app_commands.describe(motivo="informe um membro")
  async def userafk(self,interaction: discord.Integration,motivo: str=None):
    print (f"Usuario: {interaction.user.name} usou afk")
    if motivo == None:
      motivo = "ele não falou"
    afklist.append(interaction.user.id)
    afklist.append(motivo)
    resposta = discord.Embed(
      description=f"🦊┃você agora está afk!",
      colour=discord.Color.yellow()
    )
    await interaction.response.send_message(embed=resposta,ephemeral=True)


#GRUPO SERVIDOR 
  servidor=app_commands.Group(name="servidor",description="Comandos de usuarios do bot.")

#COMANDO ICONE DE SERVIDOR
  @servidor.command(name="icone", description='🗄️⠂Exibe o ícone do servidor')
  async def icone(self, interaction: discord.Interaction):
    print(f"Usuario: {interaction.user.name} usou icone do servidor")
    servidor = interaction.guild
    icone_url = servidor.icon.url if servidor.icon else None
    if icone_url:
      resposta = discord.Embed(
        title="🦊┃Ícone do Servidor",
        description=f"Aqui está o ícone do servidor: {servidor.name}",
        colour=discord.Color.yellow()
      )
      resposta.set_image(url=icone_url)
      view = discord.ui.View()
      item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Abrir em navegador", url=icone_url)
      view.add_item(item=item)
      await interaction.response.send_message(embed=resposta, view=view)
    else:
      await interaction.response.send_message("❌┃ O servidor não possui ícone.", ephemeral=True)


#COMANDO BANNER DE SERVIDOR
  @servidor.command(name="banner", description='🗄️⠂Exibe o banner do servidor')
  async def banner(self, interaction: discord.Interaction):
    print(f"Usuario: {interaction.user.name} usou banner do servidor")
    servidor = interaction.guild
    banner_url = servidor.banner.url if servidor.banner else None
    if banner_url:
      resposta = discord.Embed(
        title="🦊┃Banner do Servidor",
        description=f"Aqui está o banner do servidor: {servidor.name}",
        colour=discord.Color.yellow()
      )
      resposta.set_image(url=banner_url)
      view = discord.ui.View()
      item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Abrir em navegador", url=banner_url)
      view.add_item(item=item)
      await interaction.response.send_message(embed=resposta, view=view)
    else:
      await interaction.response.send_message("❌┃ O servidor não possui um banner.", ephemeral=True)
    

#COMANDO SPLASH DE SERVIDOR
  @servidor.command(name="splash", description='🗄️⠂Exibe a splash do servidor')
  async def splash(self, interaction: discord.Interaction):
    print(f"Usuario: {interaction.user.name} usou splash do servidor")
    servidor = interaction.guild
    splash_id = servidor.splash
    if splash_id:
        splash_url = f"{splash_id}"
        resposta = discord.Embed(
            title="🦊┃Splash do Servidor",
            description="Aqui está a splash do servidor:",
            colour=discord.Color.yellow()
        )
        resposta.set_image(url=splash_url)
        view = discord.ui.View()
        item = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Abrir em navegador", url=splash_url)
        view.add_item(item=item)
        await interaction.response.send_message(embed=resposta, view=view)
    else:
        await interaction.response.send_message("❌┃ O servidor não possui uma splash definida.", ephemeral=True)

#COMANDO INFORMAÇÂO DE SERVIDOR
  @servidor.command(name="info", description='🗄️⠂Exibe informações sobre o servidor')
  @app_commands.describe(id="informe uma id de um servidor")
  async def infoservidor(self, interaction: discord.Interaction, id: str=None):
    print(f"Usuario: {interaction.user.name} usou infoservidor")
    if id is None:
      servidor = interaction.guild
    else:
      servidor = self.client.get_guild(int(id))
      if servidor is None:
        await interaction.response.send_message("❌┃ Não achei esse servidor.", ephemeral=True)
        return
    icone_url = servidor.icon.url if servidor.icon else None
    resposta = discord.Embed(
        title=f"🦊┃Informações de {servidor.name}",
        description=servidor.description,
        colour=discord.Color.yellow()
    )
    resposta.set_thumbnail(url=icone_url)
    resposta.add_field(name=":bust_in_silhouette: Usuarios", value=f"```Total: {servidor.member_count}\nPessoas: {sum(1 for member in servidor.members if not member.bot)}\nBots: {sum(1 for member in servidor.members if member.bot)}```")
    resposta.add_field(name=":file_folder: Canais", value=f"```Total: {len(servidor.channels)}\nTexto: {sum(1 for canal in servidor.channels if isinstance(canal, discord.TextChannel))}\nVoz: {sum(1 for canal in servidor.channels if isinstance(canal, discord.VoiceChannel))}```")
    resposta.add_field(name=":crown: Dono", value=f"```{servidor.owner.name}\n{servidor.owner.id}```")
    resposta.add_field(name=":id: ID", value=f"```{servidor.id}```")
    resposta.add_field(name=":calendar: Criado em", value=f"```{servidor.created_at.strftime('%d/%m/%Y às %H:%M:%S')}```")
    resposta.add_field(name=":fox: Emojis", value=f"```Total: {len(servidor.emojis)}```")

    await interaction.response.send_message(embed=resposta)


async def setup(client:commands.Bot) -> None:
  await client.add_cog(misc(client))