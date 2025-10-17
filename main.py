# AS IMPORTAÇÔES NECESSARIAS
import discord,os, platform, datetime
from os import listdir
from discord.ext import commands
from discord.errors import HTTPException, LoginFailure
from discord import app_commands
from dotenv import load_dotenv





# Verifica se o arquivo .env existe
if not os.path.exists('.env'):
    print("O arquivo .env não foi encontrado, por favor edite o Exemplo.env para .env somente com as informações do seu bot.")
    exit()




#CARREGA E LE O ARQUIVO .env
load_dotenv() #load .env
token_bot = os.getenv("DISCORD_TOKEN") #acessa e define o token do bot
donoid = os.getenv("DONO_ID") #acessa e define a ID do dono do bot
prefixo = '-br' # Define o prefixo do bot, pode alterar se quiser





#classe basica de iniciação do bot
class Client(commands.Bot):
    def __init__(self) -> None:
        # o command_prefix está definindo um prefixo para o bot, você pode alterar caso desejar porém nessa versão não usamos nenhum prefixo
        super().__init__(command_prefix=prefixo, intents=discord.Intents().all())
        self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez
        self.cogslist = []
        #o item a baixo faz a leitura da lista de cogs que são os outros arquivos de codigo separado e os registra.        
        for cog in listdir("src/services/modules"):
            if cog.endswith(".py"):
                cog = os.path.splitext(cog)[0]
                self.cogslist.append('src.services.modules.' + cog)




    #não sei, não mexe, só sei que precisa
    async def setup_hook(self):
      for ext in self.cogslist:
        await self.load_extension(ext)




    #On_ready do bot
    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dsc.gg/braixen")) #Indica oque exibir no status do bot.
        if not self.synced: #Checar se os comandos slash foram sincronizados 
            await self.tree.sync()
            self.synced = True
            print(f"Comandos sicronizados: {self.synced}")
        print(f"🐍 - Versão do python: {platform.python_version()}")
        print(f"🦊 - O Bot {self.user} já está online e disponível")
        print(f"💖 - Estou em {len(self.guilds)} comunidades com um total de {len(self.users)} membros")
        print(f"⏰ - A hora no sistema é {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
        print(f"👤 - ID do dono é {donoid}\n\n")
    



#COISA DO MAIN NÂO MEXER

client = Client()



#LIGA O BOT e o mantem online
try:
    client.run(token_bot)
except LoginFailure as e:
    print("Erro ao fazer login: O token fornecido é inválido ou incorreto.")
except Exception as e:
    print(f"Erro desconhecido: {e}")
