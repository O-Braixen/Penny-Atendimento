import discord, os, asyncio, logging
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from src.services.connection.boosts import addBoost, changeBoost
from src.services.connection.roles import get_role_id, set_role_id
from src.services.essential.respostas import Res


load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) #load .env da raiz
donoid = int(os.getenv("DONO_ID"))
logging.basicConfig(level=logging.INFO)







class BoostManager(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client






    @commands.Cog.listener()
    async def on_ready(self):
        print("🚀 - Módulo BoostManager carregado.")











    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        servidor = after.guild
        onebooster = servidor.premium_subscriber_role
        doublebooster = servidor.get_role(get_role_id())

        if onebooster in before.roles and onebooster not in after.roles:
            await after.remove_roles(doublebooster)
            canal = after.guild.system_channel
            if canal:
                await canal.send(f"{after.mention} não é mais Booster")
            await changeBoost(after, 0)










    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild or not message.guild.system_channel:
            return

        if message.channel.id == message.guild.system_channel.id:
            if message.type in [
                discord.MessageType.premium_guild_subscription,
                discord.MessageType.premium_guild_tier_1,
                discord.MessageType.premium_guild_tier_2,
                discord.MessageType.premium_guild_tier_3
            ]:
                usuariobooster = message.author
                boosts = await addBoost(usuariobooster)

                if boosts >= 2:
                    doublebooster = message.guild.get_role(get_role_id())
                    await usuariobooster.add_roles(doublebooster)
                    await message.channel.send(f"{usuariobooster.mention} virou 2x booster")
                else:
                    await message.channel.send(f"{usuariobooster.mention} virou 1x booster")











    @app_commands.command(name="configurar-boost", description="⚙️⠂Configurar as opções de boost")
    @app_commands.default_permissions(administrator=True)
    async def configurarboost(self, interaction: discord.Interaction):
        if interaction.user.id == donoid:
            await interaction.response.send_message("Carregando...", ephemeral=True)
            try:
                doubleboosterrole = await interaction.guild.create_role(name="Double Booster")
                set_role_id(doubleboosterrole.id)

                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
                }
                created_channel = await interaction.guild.create_text_channel(
                    name="notificações-boosts", overwrites=overwrites
                )

                await interaction.guild.edit(
                    system_channel=created_channel,
                    system_channel_flags=discord.SystemChannelFlags(premium_subscriptions=True)
                )

                for member in interaction.guild.members:
                    if member.premium_since:
                        await changeBoost(member, 1)

            except Exception as e:
                await interaction.edit_original_response(
                    content=f"❌ Não foi possível finalizar a ação, erro:```{e}```"
                )
            else:
                await interaction.edit_original_response(
                    content=f"🎉 Operação concluída!\n> Cargo {doubleboosterrole.mention} criado.\n> Canal {created_channel.mention} criado."
                )
        else:await interaction.response.send_message(Res.trad_nada( str="message_erro_onlyowner"),delete_after=20,ephemeral=True)














async def setup(client: commands.Bot) -> None:
    await client.add_cog(BoostManager(client))
