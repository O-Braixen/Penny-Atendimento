import discord,os,asyncio,random,uuid
from discord.ext import commands
from discord import app_commands
from src.services.connection.database import BancoUsuarios,BancoBot
from src.services.essential.respostas import Res
from dotenv import load_dotenv

from PyCharacterAI import Client



char_id = os.getenv('char_id')
char_token = os.getenv('char_token')


clientcai = Client()




# ======================================================================

# FUNÇÃO PARA CRIAR UMA NOVA CONVERSA DO TICKET
async def create_ai_chat():
  tentativas = 10
  for tentativa in range(1, tentativas + 1):
    try:
        # AUTENTICANDO CLIENTECAI PARA ACESSAR AS COISAS NO CAI
      await clientcai.authenticate(char_token)
      chat, greeting_message = await clientcai.chat.create_chat(char_id)
      text = greeting_message.get_primary_candidate().text
      print(f"✅ Conversa criada com sucesso na tentativa {tentativa}: {text}")
      return chat.chat_id, text, True

    except Exception as e:
      print(f"⚠️ Erro na tentativa {tentativa} ao criar conversa: {e}")
      await clientcai.close_session()
      await asyncio.sleep(1)  # espera antes de tentar de novo

  print("❌ Falha após 10 tentativas de criar conversa.")
  return 0, 0, False




#FUNÇAO PARA CRIAR UMA NOVA CONVERSA DO TICKET
async def response_ai_chat(id_chat , msg ):
  tentativas = 10
  for tentativa in range(1, tentativas + 1):
    try:
      # AUTENTICANDO CLIENTECAI PARA ACESSAR AS COISAS NO CAI
      await clientcai.authenticate(char_token)
      data = await clientcai.chat.send_message(char_id, id_chat, msg)
      print(f"resposta do ai: {data.get_primary_candidate().text}")
      return data.get_primary_candidate().text
    except Exception as e:
      print(f"⚠️ Erro na tentativa {tentativa} para conversar: {e}")
      await clientcai.close_session()
      await asyncio.sleep(1)  # espera antes de tentar de novo
        
  