import discord,os,requests
from discord.ext import commands
from discord import app_commands


def getdonoid():
    return donoid
def getmensagemerro():
    return mensagemerro

donoid = 197071176810364928
mensagemerro = "<:ew:969703224825225266> Ue? Isso não funcionou como deveria... \nAcho que você tentou usar isso em um canal errado ou não tem permissão para tal função <:derp:969703169670131812>"

class onwer(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print("Cog onwer carregado.")

  #GRUPO SERVIDOR
  dono = app_commands.Group(name="onwer",description="Comandos de dono do Brix.")

  #COMANDO SAY
  @dono.command(name="say", description="🦊⠂Diga alguma coisa como Brix")
  @app_commands.describe(mensagem="Qual é a mensagem?")
  async def say(self,interaction: discord.Interaction, mensagem: str):
    print(f"Comando say - User: {interaction.user.name} - mensagem:{mensagem}")
    if interaction.user.id == donoid:
      await interaction.response.send_message("<:BN:416595378956271626>┃ enviando sua mensagem...", ephemeral=True)
      await interaction.channel.send(f"{mensagem}")
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True)

  #COMANDO LISTAR SERVIDORES
  @dono.command(name="listar", description="🦊⠂lista os servidores que o Brix está.")
  async def listservers (self,interaction: discord.Interaction):
    print (f"Usuario: {interaction.user.name} usou lista servidores")
    if interaction.user.id == donoid: # Verifica se o usuário é o dono do bot
      await interaction.response.defer () # Envia uma resposta de interação para indicar que o comando está sendo processado
      servers = self.client.guilds
      lista = "Lista de Servidores 🦊\n" # Cria uma variável para armazenar a lista de servidores
      for server in servers:
        lista += f"Nome:`{server.name}` - id:`{server.id}`\n" # Adiciona o nome e o id de cada servidor à lista, separados por uma quebra de linha
      await interaction.followup.send(content=lista) # Edita a resposta de interação com a lista de servidores
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True) # Envia uma resposta de interação que só é visível para o usuário

  #COMANDO SAIR Servidor
  @dono.command(name="sair", description="🦊⠂Faz o Brix sair de servidor.")
  @app_commands.describe(id_servidor="Qual é a Id do servidor?")
  async def leave (self,interaction: discord.Interaction,id_servidor:str):
    print (f"Usuario: {interaction.user.name} usou sair servidores")
    if interaction.user.id == donoid:
        guild = self.client.get_guild (int (id_servidor)) # Obtém o objeto guilda pelo ID
        await guild.leave () # Faz o bot sair da guilda
        await interaction.response.send_message(f"sai do {guild.name}")
    else:
        await interaction.response.send_message(mensagemerro,ephemeral=True)


  #COMANDO ALTERAR NOME BOT
  @dono.command(name="bot-name", description="🦊⠂Define um novo nome ao bot")
  @app_commands.describe(nome="Qual é o novo nome?")
  async def say(self,interaction: discord.Interaction, nome: str):
    print(f"Comando bot-name - User: {interaction.user.name} - mensagem:{nome}")
    if interaction.user.id == donoid:
      await self.client.user.edit(username=nome)
      await interaction.response.send_message(f"<:BN:416595378956271626>┃ O Nome do bot definido para {nome}", ephemeral=True)
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True)


  #COMANDO ALTERAR AVATAR BOT
  @dono.command(name="bot-avatar", description="🦊⠂Define um novo avatar ao bot")
  @app_commands.describe(avatar="Qual é o novo avatar?")
  async def say(self,interaction: discord.Interaction, avatar: discord.Attachment):
    print(f"Comando bot-avatar - User: {interaction.user.name}")
    if interaction.user.id == donoid:
      avatar = await avatar.read()
      await self.client.user.edit(avatar=avatar)
      await interaction.response.send_message(f"<:BN:416595378956271626>┃ O Avatar do bot foi redefinido", ephemeral=True)
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True)




    #GRUPO BOT 
  bot=app_commands.Group(name="brix",description="Comandos de controle do bot.")
  #COMANDO PING
  @bot.command(name="ping",description='🤖⠂Exibe o ping do Brix')
  async def ping(self,interaction: discord.Interaction):
    print (f"Usuario: {interaction.user.name} usou ping")
    resposta = discord.Embed(
            colour=discord.Color.yellow(),
            title="🏓┃Pong",
            description=f"Latencia: `{round(self.client.latency * 1000)}`ms."
        )
    await interaction.response.send_message(embed=resposta)


                  #COMANDO INFO BOT
  @bot.command(name="info",description='🤖⠂Exibe informações sobre o Brix')
  async def botinfo(self, interaction: discord.Interaction):
    print (f"Usuario: {interaction.user.name} usou botinfo")
    token = "197071176810364928-c1dced7a76c2b5c88de2b06a34ee8cb5ced572109c37cdf3093a2c3e3737e21a"
    idaplication = "a4273e10298e4f10a7f80b41061c78c5"
    res_information =  requests.get(f"https://api.squarecloud.app/v2/apps/{idaplication}", headers={"Authorization": token})
    res_information = res_information.json()
    res_status =  requests.get(f"https://api.squarecloud.app/v2/apps/{idaplication}/status", headers={"Authorization": token})
    res_status = res_status.json()
    resposta = discord.Embed(
            colour=discord.Color.yellow(),
            title=f"🦊┃Informações do {self.client.user.name}",
            description=f"{res_information['response']['app']['desc']}"
        )
    resposta.set_thumbnail(url=f"{self.client.user.avatar.url}")
    resposta.add_field(name="🖥️⠂squarecloud.app", value=f"```{res_information['response']['app']['cluster']}```", inline=True)
    resposta.add_field(name="👨‍💻⠂Linguagem", value=f"```{res_information['response']['app']['language']}```", inline=True)
    resposta.add_field(name="🦊⠂Dono", value=f"<@{donoid}>", inline=True)
    resposta.add_field(name="📊⠂Ram", value=f"```{(res_status['response']['ram'])} / {res_information['response']['app']['ram']} MB```", inline=True)
    resposta.add_field(name="🌡⠂CPU", value=f"```{res_status['response']['cpu']}```", inline=True)
    resposta.add_field(name="🕐⠂Uptime", value=f"<t:{round(res_status['response']['uptime']/1000)}:R>", inline=True)
    resposta.add_field(name="🌐⠂Rede", value=f"```{res_status['response']['network']['total']}```", inline=True)
    resposta.add_field(name="🏓⠂Ping", value=f"```{round(self.client.latency * 1000)}ms```", inline=True)
    resposta.add_field(name="🔮⠂Menção", value=f"<@{self.client.user.id}>", inline=True)

    await interaction.response.send_message(embed=resposta)


  #help comando
  @bot.command(name="help",description='🤖⠂Ajuda sobre o Brix.')
  async def help(self,interaction: discord.Integration):
    resposta = discord.Embed( 
      colour=discord.Color.yellow(),
      title="🦊┃Ajuda sobre comandos",
      description="Eiii, sabia que também tenho novos **comandos não slash**, isso mesmo agora eu tenho novos comandos sem a necessidade de usar a barra então para facilidar a sua vida eu deixei eles aqui para **você ficar sabendo das novidades.**\n\nSegue a lista\n **-fennekin** | **-braixen** | **-delphox** | **kyu** | **te amo braixen** | **hello** | **hi** | **oi** | **ia**\n\nTambém pode me marcar e perguntar algo para o Bing GPT"
    )
    await interaction.response.send_message(embed=resposta)


async def setup(client:commands.Bot) -> None:
  await client.add_cog(onwer(client))