import discord, asyncio
from discord.ext import commands, tasks
from src.services.essential.host import informação



class BotStatus(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        




    @commands.Cog.listener()
    async def on_ready(self):
        print("🤖 - Modúlo BotStatus carregado.")

         #Ligando tasks
        if not self.update_status_loop.is_running():
            await asyncio.sleep(30)
            self.update_status_loop.start()
       








    @tasks.loop(minutes=10)
    async def update_status_loop(self):
        status_list = []

        try:
            res_information, host = await informação(self.client.user.name)
            if host == "squarecloud":
                status_list.append((discord.CustomActivity(name=f"🖥️ Squarecloud - {res_information['response']['cluster']}"), discord.Status.online))
            elif host == "discloud":
                status_list.append((discord.CustomActivity(name=f"🖥️ Discloud - CLUSTER {res_information['apps']['clusterName']}"), discord.Status.online))
        except:
            print("❌ falha ao coletar dados da square para status")
        

        status_list.extend([ 
            (discord.Activity(type=discord.ActivityType.watching, name="discord.gg/braixen"), discord.Status.online),
            (discord.Activity(type=discord.ActivityType.watching, name="@obraixen no X"), discord.Status.idle),
            (discord.Activity(type=discord.ActivityType.playing, name="na Braixen's House ✨"), discord.Status.online),
            (discord.Activity(type=discord.ActivityType.watching, name=f"{len(self.client.users)} treinadores fofinhos 💛"), discord.Status.idle),
            (discord.CustomActivity(name="📞 Atendendo um treinador na BH"), discord.Status.do_not_disturb),
            (discord.CustomActivity(name="🦊 Sendo uma boa Braixen, kyuu!"), discord.Status.online),
            (discord.Activity(type=discord.ActivityType.watching, name="quem precisa de ajuda 💬"), discord.Status.online),
            (discord.CustomActivity(name="💤 Tirando uma sonequinha"), discord.Status.idle),
            (discord.CustomActivity(name="🧹 Deixando a BH cheirosinha ✨"), discord.Status.do_not_disturb),
            (discord.CustomActivity(name="📚 Estudando os protocolos da BH"), discord.Status.idle),
            (discord.Activity(type=discord.ActivityType.playing, name="com as chamas da minha varinha 🔥"), discord.Status.online),
            (discord.Activity(type=discord.ActivityType.listening, name="as histórias dos membros 💖"), discord.Status.online),
            (discord.CustomActivity(name="☕ Preparando um chá quentinho"), discord.Status.idle),
            (discord.CustomActivity(name="🎉 Organizandinho os sorteios"), discord.Status.dnd),
            (discord.Activity(type=discord.ActivityType.watching, name="o chat da comunidade 🦊"), discord.Status.online),
        ])
                


        # loop principal para trocar os status
        for activity, status in status_list:
            await self.client.change_presence(activity=activity, status=status)
            await asyncio.sleep(900)  # apenas uma vez aqui

           



async def setup(client: commands.Bot) -> None:
    await client.add_cog(BotStatus(client))