import discord,os, asyncio , datetime,pytz
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from src.services.essential.respostas import Res
from src.services.essential.host import informação,status,restart
from src.services.essential.Criador_embed import CriadorDeEmbed






def getdonoid():
    return donoid
def getmensagemerro():
    return mensagemerro






#CARREGA E LE O ARQUIVO .env na raiz
load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) #load .env da raiz
donoid = int(os.getenv("DONO_ID")) #acessa e define o id do dono
square_token = os.getenv("square_token") #acessa e define o token da square cloud
square_idaplication = os.getenv("square_idaplication") #acessa e define o id do bot na square cloud





#Mensagem de erro que será exibida sempre que um comando falhar, edite aqui e alterará tudo
mensagemerro = "<:ew:969703224825225266> Ue? Isso não funcionou como deveria... \nAcho que você tentou usar isso em um canal errado ou não tem permissão para tal função <:derp:969703169670131812>"












#inicio dessa classe
class onwer(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client











  #usando o listener para permitir que os async daqui sejam escutados pelo main.py
  @commands.Cog.listener()
  #olha o mesmo on_ready aqui para imprimir o carregamento da cog
  async def on_ready(self):
    print("Cog onwer carregado.")








  #Mensagem que será exibida caso mencione o bot.
  @commands.Cog.listener()
  async def on_message(self,message):
  # RETORNO DO BOT CASO ALGUEM MENCIONE ELE SEM MAIS NENHUMA PALAVRA ADICIONAL
    if f"<@{self.client.user.id}>" in message.content and message.author != self.client.user:
      resposta = discord.Embed( 
        colour=discord.Color.from_str('#f4de77'),
          description= "Olá sou seu bot de atendimento, você pode editar essa minha mensagem diretamente no arquivo src/services/modules/onwer.py na linha 80 e escrever oque quiser, que sempre que alguem me marcar eu falarei oque você escreveu!!"
        )
      resposta.set_author(name= "Olá, sou a {}~!".format(self.client.user.name) ,icon_url=self.client.user.avatar.url)
      resposta.set_thumbnail(url=self.client.user.avatar.url)
      resposta.set_footer(text="sua atendente personalizada",icon_url=self.client.user.avatar.url)
      await message.reply(embed=resposta)









  #GRUPO SERVIDOR - aqui estou criando um grupo de comandos
  dono = app_commands.Group(name="onwer",description="Comandos de dono do bot.")









  #COMANDO SAY - neste caso estou criando um comando dentro de um grupo
  @dono.command(name="say", description="🦊⠂Diga alguma coisa como o bot")
  @app_commands.describe(mensagem="Qual é a mensagem?") #descrição adicional
  async def say(self,interaction: discord.Interaction, mensagem: str):
    print(f"Comando say - User: {interaction.user.name} - mensagem:{mensagem}") # imprime no terminal, vai ter de monte desses
    if interaction.user.id == donoid: # Verifica se o usuário é o dono do bot
      await interaction.response.send_message("<:BN:416595378956271626>┃ enviando sua mensagem...", ephemeral=True) # Envia uma resposta de interação que só é visível para o usuário
      await interaction.channel.send(f"{mensagem}") # Envia a mensagem no canal
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True) # Envia uma resposta de erro que só é visível para o usuário







  # COMANDO EMBED
  @dono.command(name="embed", description="🦊⠂Envie um embed como Penny.")
  async def embed(self, interaction: discord.Interaction):
      # Creates a instance of EmbedCreator class
    await interaction.response.defer()
    view = CriadorDeEmbed(interacao= interaction)
    await interaction.edit_original_response(embed=view.get_default_embed, view=view)

    





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
      await self.client.user.edit(username=nome) #Edita o nome de usuario do bot
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
      await self.client.user.edit(avatar=avatar) #Edita o avatar do bot
      await interaction.response.send_message(f"<:BN:416595378956271626>┃ O Avatar do bot foi redefinido", ephemeral=True)
    else:
      await interaction.response.send_message(mensagemerro, ephemeral=True)







    #GRUPO BOT 
  bot=app_commands.Group(name="bot",description="Comandos de controle do bot.")







  #COMANDO PING
  @bot.command(name="ping",description='🤖⠂Exibe o ping do bot')
  async def ping(self,interaction: discord.Interaction):
    print (f"Usuario: {interaction.user.name} usou ping")
    resposta = discord.Embed(
            colour=discord.Color.yellow(),
            title="🏓┃Pong",
            description=f"Latencia: `{round(self.client.latency * 1000)}`ms."
        )
    await interaction.response.send_message(embed=resposta)








    #CLEAR DM comando
  @bot.command(name="limpar-dm",description='🤖⠂Limpe todas as mensagens do bot em sua DM.')
  async def cleardm(self,interaction: discord.Interaction):
    await interaction.response.send_message(content=Res.trad_nada( str='message_clear_dm'),delete_after=20,ephemeral=True)
    async for message in interaction.user.history():
      if message.author == self.client.user:
        await asyncio.sleep(1)
        await message.delete()








                  #COMANDO INFO BOT
  @bot.command(name="info",description='🤖⠂Exibe informações sobre o bot')
  async def botinfo(self, interaction: discord.Interaction):
    await interaction.response.defer()
    fuso = pytz.timezone('America/Sao_Paulo')
    now = datetime.datetime.now().astimezone(fuso)
    try:
      
      res_information , host = await informação(self.client.user.name)
      res_status, host = await status(self.client.user.name)
      

      if host == "squarecloud":
        resposta = discord.Embed(
                colour=discord.Color.from_str('#f4de77'),
                title=f"🦊┃Informações do {self.client.user.name}",
                description=f"{res_information['response']['desc']}"
            )
        resposta.set_thumbnail(url=f"{self.client.user.avatar.url}")
        resposta.add_field(name="🖥️⠂squarecloud", value=f"```{res_information['response']['cluster']}```", inline=True)
        resposta.add_field(name="👨‍💻⠂Linguagem", value=f"```{res_information['response']['language']}```", inline=True)
        resposta.add_field(name="🦊⠂Dono", value=f"<@{donoid}>", inline=True)
        resposta.add_field(name="📊⠂Ram", value=f"```{(res_status['response']['ram'])} / {res_information['response']['ram']} MB```", inline=True)
        resposta.add_field(name="🌡⠂CPU", value=f"```{res_status['response']['cpu']}```", inline=True)
        resposta.add_field(name="🕐⠂Uptime", value=f"<t:{round(res_status['response']['uptime']/1000)}:R>", inline=True)
        resposta.add_field(name="🌐⠂Rede", value=f"```{res_status['response']['network']['total']}```", inline=True)
        resposta.add_field(name="🏓⠂Ping", value=f"```{round(self.client.latency * 1000)}ms```", inline=True)
        resposta.add_field(name="🔮⠂Menção", value=f"<@{self.client.user.id}>", inline=True)
        resposta.add_field(name="🕐⠂Hora Sistema", value=f"```{now.strftime('%d/%m/%y - %H:%M')}```", inline=True)
        resposta.add_field(name="🆔⠂Bot ID", value=f"```{self.client.user.id}```", inline=True)
        resposta.add_field(name="🍀⠂Ambiente", value=f"```Produção```", inline=True)

      if host == "discloud":
        resposta = discord.Embed(
                colour=discord.Color.from_str('#f4de77'),
                title=f"🦊┃Informações do {self.client.user.name}",
                description=f"🖥️⠂Discloud - CLUSTER {res_information['apps']['clusterName']}"
            )
        resposta.set_thumbnail(url=f"{self.client.user.avatar.url}")
        resposta.add_field(name="👨‍💻⠂Linguagem", value=f"```{res_information['apps']['lang']}```", inline=True)
        resposta.add_field(name="🦊⠂Dono", value=f"<@{donoid}>", inline=True)
        resposta.add_field(name="📊⠂Ram", value=f"```{(res_status['apps']['memory'])}```", inline=True)
        resposta.add_field(name="🗄️⠂Armazenamento", value=f"```{res_status['apps']['ssd']}```", inline=True)
        resposta.add_field(name="🌡⠂CPU", value=f"```{res_status['apps']['cpu']}```", inline=True)
        resposta.add_field(name="🕐⠂Uptime", value=f"{res_status['apps']['last_restart']}", inline=True)
        resposta.add_field(name="🌐⠂Rede", value=f"```⬇️ {res_status['apps']['netIO']['down']}/⬆️ {res_status['apps']['netIO']['up']}```", inline=True)
        resposta.add_field(name="🏓⠂Ping", value=f"```{round(self.client.latency * 1000)}ms```", inline=True)
        resposta.add_field(name="🔮⠂Menção", value=f"<@{self.client.user.id}>", inline=True)
        resposta.add_field(name="🕐⠂Hora Sistema", value=f"```{now.strftime('%d/%m/%y - %H:%M')}```", inline=True)
        resposta.add_field(name="🆔⠂Bot ID", value=f"```{self.client.user.id}```", inline=True)
        resposta.add_field(name="🍀⠂Ambiente", value=f"```Produção```", inline=True)

      await interaction.followup.send(embed=resposta)
    except:
      await interaction.response.send_message("Não foi configurado corretamente as informações para coleta de informações da squarecloud, verifique o arquivo .env")











  #help comando
  @bot.command(name="help",description='🤖⠂Ajuda sobre o bot.')
  async def help(self,interaction: discord.Integration):
    resposta = discord.Embed( 
      colour=discord.Color.yellow(),
      title="🦊┃Ajuda sobre o bot",
      description="Eaeee O Braixen aqui, bem eu deixei esse comando aqui para que você pudesse editar minha mensagem no onwer.py, espero que esteja gostando do bot, qualquer coisa me procure em https://dsc.gg/braixen"
    )
    await interaction.response.send_message(embed=resposta)














async def setup(client:commands.Bot) -> None:
  await client.add_cog(onwer(client))
