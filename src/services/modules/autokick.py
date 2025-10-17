import discord, os, asyncio, logging
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from typing import List
from src.services.connection.listautokick import carregar_banlist, salvar_banlist , usuario_na_banlist , remover_usuario_da_banlist
from src.services.essential.respostas import Res







load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) #load .env da raiz
donoid = int(os.getenv("DONO_ID"))
logging.basicConfig(level=logging.INFO)











class BlackList(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.banlist = carregar_banlist()

    @commands.Cog.listener()
    async def on_ready(self):
        print("🔒 - Módulo Autokick carregado.")


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if usuario_na_banlist(self.banlist, member.id):
            await kickmember(member)
                






    banlist=app_commands.Group(name="blacklist",description="Comandos de Lista Negra da Penny.")





   
        #COMANDO DE ADICIONAR MEMBROS A LISTA NEGRA
    @banlist.command(name = 'adicionar', description='📓⠂Adiciona um Membro a lista negra.')
    @commands.has_permissions(manage_guild=True)
    async def adicionar(self, interaction: discord.Interaction, membro: discord.User):
        if interaction.user.id != donoid:
            await interaction.response.send_message(Res.trad_nada(str="message_erro_onlyowner"), delete_after=20, ephemeral=True)
            return

        if usuario_na_banlist(self.banlist, membro.id):
            await interaction.response.send_message("Esse membro já está na blacklist.")
        else:
            self.banlist.append({"id": membro.id, "nome": str(membro)})
            salvar_banlist(self.banlist)
            await interaction.response.send_message(f"{membro.mention} foi adicionado à blacklist.")












        #COMANDO DE REMOVER MEMBROS A LISTA NEGRA
    @banlist.command(name = 'remover', description='Remove um Membro a lista negra.')
    @commands.has_permissions(manage_guild=True)
    async def remover(self, interaction: discord.Interaction, membro: str):
        if interaction.user.id != donoid:
            await interaction.response.send_message(Res.trad_nada(str="message_erro_onlyowner"), delete_after=20, ephemeral=True)
            return

        membro_id = int(membro)
        if not usuario_na_banlist(self.banlist, membro_id):
            await interaction.response.send_message("Esse membro não está na blacklist.")
        else:
            self.banlist = remover_usuario_da_banlist(self.banlist, membro_id)
            salvar_banlist(self.banlist)
            await interaction.response.send_message(f"<@{membro_id}> foi removido da blacklist.")




    # Autocomplete para ID de registro
    @remover.autocomplete("membro")
    async def remover_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        sugestoes = []
        for entry in self.banlist:
            sugestoes.append(app_commands.Choice(
                name=f"{entry['nome']} ({entry['id']})", value=str(entry['id'])
            ))
        if not sugestoes:
            sugestoes.append(app_commands.Choice(name="Sem usuários na lista negra...", value=""))
        return sugestoes



















        #COMANDO DE LISTAR MEMBROS A LISTA NEGRA
    @banlist.command(name = 'listar', description='Lista todos que estão na lista negra.')
    @commands.has_permissions(manage_guild=True)
    async def listar(self, interaction: discord.Interaction):
        if interaction.user.id != donoid:
            await interaction.response.send_message(Res.trad_nada(str="message_erro_onlyowner"), delete_after=20, ephemeral=True)
            return

        if not self.banlist:
            await interaction.response.send_message("A blacklist está vazia.")
            return

        membros = [f"- {entry['nome']} (`{entry['id']}`)" for entry in self.banlist]
        await interaction.response.send_message("**Blacklist:**\n" + "\n".join(membros))






async def kickmember(member: discord.Member):
    try:
        #envio de mensagem em DM para avisar.
        resposta = discord.Embed(
            colour=discord.Color.yellow(),
            description=f"### Oiiie~! Aqui é a Penny, atendente da Braixen's House. 💛\n\nOlá, {member.name}! Eu verifiquei aqui e parece que seu usuário está na nossa **lista de restrições**... por isso, infelizmente, não é permitido o acesso às comunidades da Braixen's House. 😔\n\nVocê foi removido automaticamente como medida de segurança, tá bom?"
            )
        resposta.set_thumbnail(url="https://media.discordapp.net/attachments/1260734744174526495/1260734958402539591/ixqtABY.webp?ex=686f9fad&is=686e4e2d&hm=719de01e3e17ec9946fbdf979014b53e6994383393172219ceca7dcc68a0299e&=&format=webp")
        await member.send(embed=resposta)

    except: print(f"Falha ao avisar na DM de {member.name} - {member.id}.")
    try:
        await asyncio.sleep(1)
        await member.kick(reason="Usuário na blacklist da BH.")
        print(f"{member.name} foi kickado (na blacklist).")
    except Exception as e:
        print(f"Erro ao kickar {member.name}: {e}")






async def setup(client: commands.Bot) -> None:
    await client.add_cog(BlackList(client))
