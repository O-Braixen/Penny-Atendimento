# AS IMPORTAÇÔES NECESSARIAS
import discord,os
from os import listdir
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

#CARREGA E LE O ARQUIVO .env
load_dotenv() #load .env
token_bot = os.getenv("DISCORD_TOKEN") #acessa e define o token do bot

#classe basica de iniciação do bot
class Client(commands.Bot):
    def __init__(self) -> None:
        # o command_prefix está definindo um prefixo para o bot, você pode alterar caso desejar porém nessa versão não usamos nenhum prefixo
        super().__init__(command_prefix='-br', intents=discord.Intents().all())
        self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez
        self.cogslist = []
        #o item a baixo faz a leitura da lista de cogs que são os outros arquivos de codigo separado e os registra.        
        for cog in listdir("cogs"):
            if cog.endswith(".py"):
                cog = os.path.splitext(cog)[0]
                self.cogslist.append('cogs.' + cog)

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
        print(f"\no Bot {self.user} Já esta Online e disponivel")
    

#COISA DO MAIN NÂO MEXER
client = Client()

#LIGA O BOT e o mantem online
client.run(token_bot)