import discord,os,asyncio, string , random ,re
from discord.ext import commands , tasks
from discord import app_commands,utils
from datetime import datetime,timedelta,timezone
from src.services.modules.owner import getdonoid,getmensagemerro
from src.services.essential.respostas import Res
from src.services.essential.cai import create_ai_chat,response_ai_chat
from dotenv import load_dotenv







#GET INFO USO
donoid = getdonoid()
mensagemerro = getmensagemerro()







#CARREGA E LE O ARQUIVO .env na raiz
load_dotenv(os.path.join(os.path.dirname(__file__), '.env')) #load .env da raiz










#VARIAVEIS NECESSARIAS
#Parte do Braixen's House
id_cargo_atendente = int(os.getenv("id_cargo_atendente")) #Coloque aqui o ID do cargo de atendente do primeiro servidor
id_atendimento_principal = int(os.getenv("id_atendimento_principal")) #Coloque aqui o ID do canal onde deseja que os tickets sejam criados (para primeiro servidor)
id_servidor_bh = int(os.getenv("id_servidor_bh")) #ID do primeiro servidor
id_canal_logs_bh = int(os.getenv("id_canal_logs_bh")) #ID do canal de logs do primeiro servidor
id_canal_avaliacao = int(os.getenv("id_canal_avaliacao")) #ID do canal para envio das avaliações





#Parte do Segundo servidor
id_cargo_tribunal = int(os.getenv("id_cargo_tribunal")) #Coloque aqui o ID do cargo de atendente do segundo servidor
id_atendimento_tribunal = int(os.getenv("id_atendimento_tribunal")) #Coloque aqui o ID do canal onde deseja que os tickets sejam criados (para Segundo servidor)
id_servidor_tribunal= int(os.getenv("id_servidor_tribunal")) #ID do segundo servidor
id_canal_logs_tri= int(os.getenv("id_canal_logs_tri")) #ID do canal de logs do segundo servidor






#Variaveis de USO GLOBAL| Se Quiser editar só edite o emojiglobal blz, o resto deixe do jeito que está
emojiglobal = "🦊"
tipoticket = "1"
staff = "1"
instrucaoIA = "1"
categoriadeatendimento = "1"
botname = "1"
botavatar = "1"





















#Gerador de ID de 6 digitos
def gerar_id_unica(tamanho=6):
    caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e números
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

























#PAINEIS DE USO NAS COMUNIDADES
#PAINEL SUPORTE BRAIXEN HOUSE
class suporte_bh(discord.ui.Select): #a class aqui recebeu o nome de Dropdown para cada classe tem que ter Nomes diferentes viu nos proximos você vai ver que eu mudei
    def __init__(self):
        options = [ #Opções do dropdown (Aqui são listadas todas as opções do menu pode adicionar ou remover se necessario) divirta-se
            
            #Ajuda adicional Value(condição para buscar resposta no Callback)| Label (texto que será exibido no menu no chat do discord) | Emoji (é só o emoji)
            
            discord.SelectOption(value="duvidas",label="Dúvidas sobre temas gerais.", emoji="⁉️"),
            discord.SelectOption(value="denuncia",label="Faça uma Denúncia.", emoji="🚨"),
            discord.SelectOption(value="bugs",label="informe um bug no servidor.", emoji="🐞"),
            discord.SelectOption(value="solicitacao",label="Solicitações de cargos ou conversões.", emoji="🔔"),
            discord.SelectOption(value="premiacao",label="Resgatar um prêmio de evento.", emoji="🎁"),
            discord.SelectOption(value="vip",label="Compre seu vip.", emoji="🌟"),
            discord.SelectOption(value="sugestao",label="Envie uma sugestão.", emoji="💡"),
            discord.SelectOption(value="parceria",label="Desejo divulgar no Braixen's House.", emoji="🤝"),
            discord.SelectOption(value="Staff",label="Vire um Staff no Braixen's House.", emoji="💼"),
            discord.SelectOption(value="outros",label="Nenhuma das opções acima.", emoji="🦊"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...", #Placeholder exibe um texto padrão quando não é selecionado nada pelo usuario
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help" #a ID do seu Dropdown | Importante caso tenha mais de 1 viu pois você tem que editar ele
        )








    async def callback(self, interaction: discord.Interaction): #Retorno do que foi selecionado no menu Dropdown
        # global = to puxando variaveis de fora do codigo para editar elas aqui, são as que estão na linha 5 a 19
        global emojiglobal #Puxa a variavel emoji global para editar posteriormente
        global tipoticket #Puxa a variavel do tipo de ticket para editar posteriormente
        global staff #Puxa a variavel staff para editar posteriormente
        global instrucaoIA #Puxa a variavel de instrução ia para editar posteriormente

        #Abaixo são as condições elas vão usar o VALUE para entrar em uma condição
        if self.values[0] == "duvidas": # < puxo o valor selecionado e verifico se ele é igual a duvidas se sim ele roda a condição, se não ele vai para as proximas.
            emojiglobal = "⁉️" #definindo o emoji antes "1" para o ⁉️
            tipoticket = "Ticket de dúvidas" #definindo o tipo de ticket
            staff = id_cargo_atendente #indicando qual é o staff para esse ticket
            instrucaoIA = "1" #Define uma instrução que será usada pela inteligencia articifial, como uma explicação do que ela tem que fazer.
            await interaction.response.send_message("**Dúvidas Gerais?** \n\nSabia que temos um canal exclusivo onde você pode ser ajudado por todos. \nTodas as dúvidas estão centralizadas em <#1027376614054576138> e você pode pesquisar lá dentro, se não tiver sua dúvida você mesmo pode postar lá e aguardar alguém te responder.",ephemeral=True) #resposta para a interação texto padrão com o ephemeral ativado (ephemeral é aquelas mensagem que só o proprio membro ve)
    # Daqui para baixo e copia e cola mudando as variaveis, lembre-se as opções aqui devem iniciar primeiro com um if (linha 74) e depois tudo com elif blz, e a quantidade de opções aqui deve ser igual ao dropdown lá em cima, cada dropdown lá tem que ter uma condição aqui.
    # o CreateTicket é o botão de abertura de ticket, aqui puxamos ele mas o codigo dele ta lá em baixo perdido.
        elif self.values[0] == "denuncia":
            emojiglobal = "🚨"
            tipoticket = "Ticket de Denúncias"
            staff = id_cargo_atendente
            instrucaoIA = "Ticket de denuncia, peça ao usuario que forneça informações claras de quem ele ta denunciando como capturas de tela, ID de usuario e seja sensivel com ele, responda com empatia e após receber tudo indique que o usuario precisa aguardar um atendente humano chegar para continuar o atendimento,não continue o atendimento sozinha"
            await interaction.response.send_message("**Deseja denúciar alguém?** \n\nPara **denúnciar** alguém por favor tenha em maos **motivo da denúncia, autor (usuario ou ID) e provas.** \n\nPara prosseguir com sua denúncia abra o ticket abaixo.",ephemeral=True,view=CreateTicket())
      
        elif self.values[0] == "bugs":
            emojiglobal = "🐞"
            tipoticket = "Ticket de Bugs e Problemas"
            staff = id_cargo_atendente
            instrucaoIA = "Ticket de bugs, peça ao usuario que forneça informações claras de qual bug ele achou, como capturas de tela e explicação clara de como ele ta presenciando aquele bug, após receber tudo indique que o usuario precisa aguardar um atendente humano chegar para continuar o atendimento,não continue o atendimento sozinha"
            await interaction.response.send_message("**Encontrou um bug em nosso servidor?** \n\nPara reportar um bug em nosso servidor tenha em mãos o **maximo de detalhes** sobre o bug relatado, inclua **capturas de tela** e **descreva detalhadamente.** \nAbra o ticket com o botão abaixo.",ephemeral=True,view=CreateTicket())
        
        elif self.values[0] == "solicitacao":
            emojiglobal = "🔔"
            tipoticket = "Ticket de Solicitações"
            staff = id_cargo_atendente
            instrucaoIA = "Ticket de Solicitações, nesse caso sinta-se livre para perguntar o motivo da solicitação dele, pode ser alteração de cargo, migração de perfil , solicitação de registros, dentre outros, em caso de dúvidas não continuar o atendimento sozinha, indique para o usuario aguardar um atendente humano."
            await interaction.response.send_message("**Solicitações?** \n\nVocê pode solicitar por varios serviços como por exemplo: \n\n*Mudanças no servidor.* \n*Novos cargos. *\n*Novas Categorias.* \n*Novos Canais.* \n\nAbra o ticket com o botão abaixo.",ephemeral=True,view=CreateTicket())

        elif self.values[0] == "premiacao":
            emojiglobal = "🎁"
            tipoticket = "Ticket de Retirada de Prêmios"
            staff = id_cargo_atendente
            instrucaoIA = "Ticket de Retirada de Prêmios, questione ao usuario qual premio ele ganhou, pergunte também se ele chegou a ler todo o regularmento caso o sorteio tenha, e por fim aguarde o atendimento humano."
            await interaction.response.send_message("**Ganhou um Prêmio?** \n\nRetire aqui mesmo seu prêmio de eventos realizados e que sejam entregues pelo Braixen's House. \nAbra o ticket com o botão abaixo.",ephemeral=True,view=CreateTicket())
        
        elif self.values[0] == "sugestao":
            emojiglobal = "💡"
            tipoticket = "Ticket de Sugestões"
            staff = id_cargo_atendente
            instrucaoIA = "1"
            await interaction.response.send_message("**Sugestões?** \n\nSabia que temos um canal exclusivo para o envio de sugestões. \nTodas as Súgestões estão centralizadas no <#1027376614054576138> você pode filtrar sua busca ou escrever uma do zero, mas seja bastante detalhista em sua sugestão blz.",ephemeral=True)
        
        elif self.values[0] == "parceria":
            emojiglobal = "🤝"
            tipoticket = "Ticket de divulgações"
            staff = id_cargo_atendente
            instrucaoIA = "Ticket de parceria, diga ao usuario que novos parceiros precisam passar por uma avaliação de requisitos, uma taxa simbólica pela divulgação, e que toda parceria vem acompanhada de um sorteio especial. Deve orientar o usuário a ler o canal <#982990181307142174> para entender os protocolos e pedir que envie o final do link do convite da comunidade (sem o discord.gg/), pois o automod apaga links completos."
            await interaction.response.send_message("**Deseja divulgar algo no Braixen's House?** \nPara **divulgar seu servidor, bot ou outros projetos.**\nO *Braixen's House* pode **te ajudar com isso** mas estamos **sujeito a avaliação de requisitos** e a possiveis **cobranças pela sua divulgação**. \n\nNesta Modalidade **todas as parcerias** precisam ser feitas em conjunto com um **sorteio** pois será dessa forma que iremos efetuar **sua divulgação.**\n**Visite o Canal** de <#982990181307142174> e **confirá os topicos 2 e 3** que informamos com detalhes como **funciona e como avaliamos**.\n\n **Não abra o ticket sem ler sobre nosso protocolo.**",ephemeral=True,view=CreateTicket())
        
        elif self.values[0] == "Staff":
            emojiglobal = "💼"
            tipoticket = "Ticket de Formulário staff"
            staff = id_cargo_atendente
            instrucaoIA = "1"
            await interaction.response.send_message("**Deseja fazer parte do time Braixen's house?** \n\nSabia que temos um formulário para quem está interessado em se tornar um staff você pode abrir ele e verificar se estamos aceitando novos formulários, Olha ta aqui o link: \nhttps://docs.google.com/forms/d/e/1FAIpQLSeZGFDS7g5oiaFV6lE2KiErLCAQXazW3SY9tieWeT5zrlOF5g/viewform?usp=sf_link",ephemeral=True)

        elif self.values[0] == "vip":
            emojiglobal = "🌟"
            tipoticket = "Ticket de Compra de vip"
            staff = id_cargo_atendente
            instrucaoIA = "Ticket de parceria, diga ao usuario que novos parceiros precisam passar por uma avaliação de requisitos, uma taxa simbólica pela divulgação, e que toda parceria vem acompanhada de um sorteio especial. Deve orientar o usuário a ler o canal <#982990181307142174> para entender os protocolos e pedir que envie o final do link do convite da comunidade (sem o discord.gg/), pois o automod apaga links completos."
            await interaction.response.send_message("**Deseja Comprar seu Vip?** \n\nPara comprar seu vip mensal abra um ticket com o botão abaixo.\n\n*Sabia que você pode comprar a assinatura vitalícia diretamente pela loja do Tails usando `T!buy 1` super simples e fácil* ",ephemeral=True,view=CreateTicket())

        
        elif self.values[0] == "outros":
            emojiglobal = "🦊"
            tipoticket = "Ticket de Outros Motivos"
            staff = id_cargo_atendente
            instrucaoIA = "Ticekt de Outros Motivos, você não sabe porque o usuario abriu ticket, então sinta-se livre para perguntar a ele, seja carismatica e caso não sabia de algo peça para o usuario aguardar outro atendente."
            await interaction.response.send_message("**Não tem sua Questão?** \n\nNão tem problema, por favor crie um ticket clicando no botão abaixo",ephemeral=True,view=CreateTicket())








# UFAAA, se chegou até aqui seu primeiro painel já está quase configurado eu acho, daqui para baixo é mais coisa importante viu.

















#PAINEIS PERSISTENTES 
# Isso aqui é importante, essa parte aqui indica que os paineis que criamos devem ser pesistentes, então toda vez que você reiniciar seu bot e já tiver um painel criado ele automaticamente puxa o já existente, assim você não precisa criar um novo toda vez blz.
# CADA DROPDOWN deve receber um custom_id diferente então elas são diferentes para não confundir esse cara aqui, se elas forem iguais vai bugar esse cara

#PAINEl PERSISTENTES SUPORTE BRAIXEN HOUSE
class DropdownSuporte(discord.ui.View): # Olha a classe aqui, ela é diferente das lá de cima blz.
    def __init__(self): #não me pergunta pq eu não sei oque é só coloca que precisa.
        super().__init__(timeout=None) #isso aqui define o tempo que o painel vai expirar, nesse caso none é NUNCAAAAA.
        self.add_item(suporte_bh())#isso aqui eu to falando que ele vai adicionar o dropdown de novo em caso de reinicio.
















# PAINEL DO TRIBUNAL PARA O SEGUNDO SERVIDOR | esse é usado no segundo servidor blz mas é copia e cola dos outros só mudando as variaveis.
class tribunal_bh(discord.ui.Select): # CLASSEE EDITADA DE NOVOOOOOO BIRL Dropdown3 agora
    def __init__(self):
        options = [#Opções do dropdown qe vão aparecer no dropdown
            discord.SelectOption(value="questionar",label="Quero questionar meu ban.", emoji="🔨"),
            discord.SelectOption(value="duvidas",label="Tenho dúvidas sobre meu ban.", emoji="❓"),
            discord.SelectOption(value="regras",label="Dúvidas sobre as regras.", emoji="📋"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_tribunal" #Olha a porra da ID aqui de novo e ela ta diferente viuuuu lembra disso que vamos usar depois
        )
    async def callback(self, interaction: discord.Interaction): #Retorno seleção Dropdown do painel do tribunal

        #(CTRL+V) mesma coisa do de cima, Puxando variaveis para usar e editar rsrsrs
        global emojiglobal
        global tipoticket
        global staff
        global instrucaoIA
        
        # Aqui é igualzinho aos outros, só muda as condições 🤙
        if self.values[0] == "questionar":
            emojiglobal = "🔨"
            tipoticket = "Ticket de Questionamento de Banimento"
            staff = id_cargo_tribunal
            instrucaoIA = "Ticket de Questionamento de Banimento, o usuario que você vai atender foi banido da Braixen's House, peça para ele a ID de usuario, o Horario que foi banido caso ele saiba e aguarde um atendente chegar."
            await interaction.response.send_message("**Deseja Questionar o seu banimento?** \n\nSe você foi banido do Braixen's House e acredita que seu banimento tenha sido injusto.\n\nabre um ticket ai e vamos revisar o seu caso.",ephemeral=True,view=CreateTicket())
       
        elif self.values[0] == "duvidas":
            emojiglobal = "❓"
            tipoticket = "Ticket de Dúvidas"
            staff = id_cargo_tribunal
            instrucaoIA = "nada"
            await interaction.response.send_message("**Está com dúvidas sobre o seu banimento?** \n\nBom todos os registros do Braixen's House estão disponívels de forma replicada neste servidor, no Canal <#1046777277582692393>.\n\nCaso você não entenda o motivo do seu banimento abra a opção de Questionar seu banimento e vamos exclarecer a todas as suas dúvidas.",ephemeral=True)
        
        elif self.values[0] == "regras":
            emojiglobal = "📋"
            tipoticket = "Ticket de Outras Solicitações"
            staff = id_cargo_tribunal
            instrucaoIA = "nada"
            await interaction.response.send_message("**Você tem dúvidas sobre as regras?** \n\nNão se preocupe, todas elas estão em <#1046764161398493340>.",ephemeral=True)










#PAINEL PERSISTENTE TRIBUNAL BRAIXEN HOUSE - igualzinho, mas puxa o tribunal
class DropdownTribunal(discord.ui.View):
    def __init__(self): 
        super().__init__(timeout=None)
        self.add_item(tribunal_bh())


























#BOTÔES DOS PAINEIS DE ATENDIMENTO
#BOTÂO CRIAR TICKET
#lembra do botão que puxamos lá em cima em um monte de opção, ele ta aquiiii
class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value=None

     # visual do botão aqui, label é o texto que vai estar no botão| Style é a cor, consulte a documentação pois tem cores especificas | Emoji é o emoji do botão
    @discord.ui.button( label="Abrir Atendimento", style=discord.ButtonStyle.blurple, emoji="🔓"    )
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        global emojiglobal, staff, instrucaoIA
        self.value = True
        self.stop()

        # VERIFICA SE JÁ EXISTE UM ATENDIMENTO ABERTO
        canal_principal = interaction.channel
        # Padrão base que identifica o usuário, ignorando o emoji e categoria
        identificador_usuario = f"{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.id}"

        # Procura qualquer thread ativa do usuário
        thread_ativa = None
        for t in canal_principal.threads:
            if identificador_usuario in t.name and not t.archived and not t.locked:
                thread_ativa = t
                break  # já achou uma ativa, pode parar
        # VERIFICA SE A THREAD ESTA ATIVA, SE TIVER FORÇA O USUARIO A FICAR NELA
        if thread_ativa:
            view = discord.ui.View()
            item = discord.ui.Button( style=discord.ButtonStyle.gray, label=f"Atendimento de {interaction.user.name.lower().replace(' ', '-')}", url=f"https://discord.com/channels/{interaction.guild.id}/{thread_ativa.id}" )
            view.add_item(item=item)
            await interaction.response.send_message( Res.trad_nada(str="message_abrir_ticket_user").format(thread_ativa.mention), ephemeral=True, delete_after=20, view=view )
            await thread_ativa.send( Res.trad_nada(str="message_abrir_ticket_channel").format(interaction.user.mention)  )
            await thread_ativa.send("<:BH_Braix_You:1154338867068010528>")
            return
                

        # Cria uma thread privada
        thread = await canal_principal.create_thread( name=f"{emojiglobal}┃{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.id}", type=discord.ChannelType.private_thread, invitable=False )
        # Mensagem de confirmação com botão
        view = discord.ui.View()
        item = discord.ui.Button(style=discord.ButtonStyle.gray,label=f"Atendimento de {interaction.user.name.lower().replace(' ', '-')}",url=f"https://discord.com/channels/{interaction.guild.id}/{thread.id}")
        view.add_item(item=item)
        await interaction.response.send_message( ephemeral=True, delete_after=10, content=f"<:BH_Braix_Happy4:1154338634011521054> Ticket criado com sucesso! 🎉", view=view )

        # Mensagens iniciais da thread
        await thread.send(f"Avisando:<@{interaction.user.mention}> e colocando os <@&{staff}>")
        await thread.purge(limit=1)


        # CASO NÃO TENHA TICKET ABERTO CONTINUA AQUI E CRIA UMA 
        idatendimento = gerar_id_unica()
        aiid , msg , check  = await create_ai_chat()

        embedticket = discord.Embed( colour=discord.Color.from_str('#f4de77'),
            description=f"Atendimento: **{tipoticket}**\nResponsavel: <@&{staff}>\nID: **{idatendimento}**\nAtendente Atual: {interaction.client.user.name if check else '0'}\nAIID: {aiid}"
        )
        #embedticket.set_author(name=f"{interaction.client.user.name}", icon_url=f"{interaction.client.user.display_avatar.url}")
        embedticket.set_thumbnail(url="https://i.imgur.com/ixqtABY.png")
        embedticket.set_footer(text="Use o botão Finalizar Atendimento para encerrar seu atendimento!")

        await thread.send(embed=embedticket, view=FinalizarTicket())
        instrucao = f"você está iniciando o atendimento do usuario {interaction.user.name} marca ele enviando {interaction.user.mention} e responda a ele de forma amigavel para iniciar uma conversa, informe que pode usar bots no canal, evite usar termos relacionados a horarios e o motivo do contato dele é {instrucaoIA}, apenas inicie o atendimento sem confirmar nada a essa mensagem."
        if check:
            async with thread.typing():
                await thread.send(msg)
           
            msg_ai = await response_ai_chat(aiid,instrucao)
            
            async with thread.typing():
                await thread.send(msg_ai)
        
        else: # RETORNO PADRÂO CASO FALHE O PEDIDO DE IA
            await thread.send("Kyu~! Minha inteligência artificial está indisponível no momento 💛\nPor favor, descreva sua solicitação e aguarde que um atendente humano irá ajudá-lo em breve, tá bem? 🌸")

























# BOTÃO FINALIZAR TICKET
class FinalizarTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button( label="Finalizar", style=discord.ButtonStyle.blurple, emoji="🔒", custom_id="finalizar" )
    async def finalizar(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            membro_id = interaction.channel.name.split('-')[-1]
            membro = interaction.guild.get_member(int(membro_id))

            if interaction.user == membro or any( role.id in [id_cargo_atendente, id_cargo_tribunal] for role in interaction.user.roles ):
                self.value = True
                self.stop()
                await interaction.response.send_message(f"Oi oi, {membro.mention}! 🌸")
                await asyncio.sleep(0.7)

                await interaction.channel.send("Hmm… parece que estamos chegando ao final do seu atendimento, kyu~ 💛")
                await asyncio.sleep(1.0)

                await interaction.channel.send("A **Braixen's House** fica muito feliz pelo seu contato! Espero que tenha tirado todas as suas dúvidas, kyu~ 🦊")
                await asyncio.sleep(0.8)

                await interaction.channel.send("Antes de fechar, que tal deixar sua avaliação sobre o atendimento? Depois é só finalizar o ticket, tá bem? 🌸", view=DeleteTicket())
                await asyncio.sleep(0.5)

                await interaction.channel.send("Ahh! E não se preocupe, se precisar de algo mais, é só abrir um novo ticket que eu estarei aqui rapidinho, kyu~ 💛")

            else:
                await interaction.response.send_message(Res.trad_nada(str="message_erro_onlyStaff/Solicitante"),delete_after=20,ephemeral=True)
        except:
            await interaction.response.send_message(Res.trad_nada(str="mensagem_erro"),delete_after=20,ephemeral = True)

    @discord.ui.button(label="+", style=discord.ButtonStyle.green, emoji="👤", custom_id="adicionar")
    async def adicionar(self, interaction: discord.Interaction, button: discord.ui.Button):
        mod = interaction.guild.get_role(id_cargo_atendente)
        mod2 = interaction.guild.get_role(id_cargo_tribunal)
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.user.roles or mod2 in interaction.user.roles:
            await interaction.response.send_message(Res.trad_nada(str="message_add_user_ticket"),delete_after=120,view=DropdownMembro(interaction, action='adicionar'))
        else:
            await interaction.response.send_message(Res.trad_nada(str="message_erro_onlyStaff/Solicitante"),delete_after=20,ephemeral=True)


    @discord.ui.button(label="-", style=discord.ButtonStyle.red, emoji="👤", custom_id="remover")
    async def remover(self, interaction: discord.Interaction, button: discord.ui.Button):
        mod = interaction.guild.get_role(id_cargo_atendente)
        mod2 = interaction.guild.get_role(id_cargo_tribunal)
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.user.roles or mod2 in interaction.user.roles:
            await interaction.response.send_message(Res.trad_nada(str="message_rem_user_ticket"),delete_after=120,view=DropdownMembro(interaction, action='remover'))
        else:
            await interaction.response.send_message(Res.trad_nada(str="message_erro_onlyStaff/Solicitante"),delete_after=20,ephemeral=True)

















# Dropdown de gerenciamento de membros
class DropdownMembro(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, action: str):
        super().__init__(timeout=None)
        self.add_item(DropdownSelect(action=action))


class DropdownSelect(discord.ui.UserSelect):
    def __init__(self, action):
        self.action = action
        super().__init__(placeholder="Escolha um membro...", min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        membro = interaction.guild.get_member(self.values[0].id)
        if self.action == 'adicionar':
            await interaction.channel.add_user(membro)
            await interaction.response.send_message(Res.trad_nada(str="message_add_user_send").format(membro.mention) , ephemeral=True)
        elif self.action == 'remover':
            await interaction.channel.remove_user(membro)
            await interaction.response.send_message(Res.trad_nada(str="message_rem_user_send").format(membro.mention) , ephemeral=True)


















# Função de fechamento de thread (remove usuário, renomeia e arquiva)
async def encerrar_thread(thread: discord.Thread, servidor: discord.Guild, membro: discord.Member):
    try:
        # Tenta pegar a primeira mensagem (que contém o embed do ticket)
        primeira_msg = [m async for m in thread.history(limit=2, oldest_first=True)][0]
        print(primeira_msg)
        id_ticket = None

        if primeira_msg.embeds:
            embed = primeira_msg.embeds[0]
            if embed.description:
                match = re.search(r"ID:\s+\*\*(.*?)\*\*", embed.description)
                print(match)
                if match:
                    id_ticket = match.group(1)

        # Renomeia com o formato desejado
        if id_ticket:
            novo_nome = f"{id_ticket} - {membro.id}"
            await thread.edit(name=novo_nome)
            print(f"[LOG] Thread renomeada para {novo_nome}")
        else:
            print("[AVISO] Nenhum ID encontrado no embed do ticket.")
    except Exception as e:
        print(f"[ERRO] Falha ao renomear thread: {e}")

    # Remove todos os membros, exceto o bot
    try:
        async for participante in thread.fetch_members():
            if participante.id != thread.guild.me.id:
                try:
                    await thread.remove_user(participante)
                except:
                    pass
    except Exception as e:
        print(f"[ERRO] Falha ao remover membros: {e}")

    # Envia mensagem final e sai da thread
    try:
        await thread.send(Res.trad_nada(str="message_confirm_arquivamento"))
        await asyncio.sleep(2)
    except:
        pass

    # Arquiva, tranca e o bot sai da thread
    try:
        await thread.edit(archived=True, locked=True)
        await asyncio.sleep(1)
        await thread.leave()
        print(f"[LOG] Thread {thread.name} encerrada e o bot saiu com sucesso.")
    except Exception as e:
        print(f"[ERRO] Falha ao arquivar/sair da thread: {e}")





















#Botão deletar ticket
class DeleteTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value=None




    @discord.ui.button(label="Avaliar Atendimento",style=discord.ButtonStyle.blurple,emoji="<:BH_staffmesbadge:1154180188582727832>",custom_id="avaliar")
    async def buttonavaliar(self,interaction: discord.Interaction, button: discord.ui.Button):     
        self.value = True 
        await interaction.response.send_message(Res.trad_nada(str="message_avaliar_atendimento"),delete_after=15,ephemeral=True)   
    


    @discord.ui.button(label="Encerrar Ticket",style=discord.ButtonStyle.red,emoji="<:BH_Braix:1154338509839143023>",custom_id="encerrar")#ESPECIFICAÇÂO DO BOTÂO
    async def confirm(self,interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

        mod = interaction.guild.get_role(id_cargo_atendente)
        mod2 = interaction.guild.get_role(id_cargo_tribunal)
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.user.roles or mod2 in interaction.user.roles:
            await interaction.response.send_message(Res.trad_nada(str="message_encerrar_ticket"),ephemeral=True)
            await asyncio.sleep(2)
            membro_id = interaction.channel.name.split('-')[-1]
            usuario = interaction.client.get_user(int(membro_id))
            await encerrar_thread( interaction.channel, interaction.guild ,usuario) 
            try:
                resposta = discord.Embed( colour=discord.Color.from_str('#f4de77'), description=Res.trad_nada(str="message_encerrar_ticket_embed_description"))   
                resposta.set_thumbnail(url="https://i.imgur.com/ixqtABY.png")
                resposta.set_footer(text=Res.trad_nada(str="message_encerrar_ticket_embed_footer"))
                await usuario.send(embed=resposta)
            except: print(f"falha ao agradecer o membro {membro_id}")
        else:
            # se falso manda isso ai em baixo
            await interaction.response.send_message(mensagemerro)

















#INICIO DA CLASSE
class atendimento(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:

        #Aqui estou criando uma variavel global para usar em outra 
        global botname
        global botavatar
        self.client = client
        botname = self.client.user.name
        botavatar = self.client.user.avatar

        #Carrega os menu e adiciona eles
        self.menu_atendimento = app_commands.ContextMenu(name="Abrir Atendimento",callback=self.abrirticketmenu)
        self.client.tree.add_command(self.menu_atendimento)
        self.client.add_view(DropdownSuporte())  #carrega o Painel de Suporte
        self.client.add_view(DropdownTribunal()) #carrega o painel de tribunal
        self.client.add_view(FinalizarTicket())
















    @commands.Cog.listener()
    async def on_ready(self):
        print("📞 - Modúlo atendimento carregado.")
        await asyncio.sleep(15)
        self.check_inactive_channels.start() #Verificador de atendimentos inativos
    
    




    #Remove os menu se necessario
    async def cog_unload(self) -> None:
        self.client.tree.remove_command(self.menu_atendimento, type=self.menu_atendimento.type)
  















    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # PARTE DA IA PARA RESPONDER TICKET
        # Verifica se a mensagem foi enviada dentro de uma thread (ticket)
        if not isinstance(message.channel, discord.Thread):
            return


        # Verifica se é uma thread ativa (não arquivada nem trancada)
        if message.channel.archived or message.channel.locked:
            return

        # Pega a 2ª mensagem da thread (onde está o embed original)
        try:
            mensagens = [m async for m in message.channel.history(limit=2, oldest_first=True)]
            embed_msg = mensagens[0]
        except Exception as e:
            print(f"Erro ao buscar mensagens do ticket: {e}")
            return

        # Verifica se há embed e se ele segue o padrão
        if not embed_msg.embeds:
            return

        embed = embed_msg.embeds[0]
        desc = embed.description or ""
        linhas = desc.split("\n")

        # Garante que o embed tem os campos necessários
        if not any("ID:" in linha for linha in linhas) or not any("Atendente Atual:" in linha for linha in linhas):
            return

        # Extrai o ID do ticket, atendente atual e AIID
        id_ticket = None
        atendente_atual = None
        aiid = None

        for linha in linhas:
            if linha.startswith("ID:"):
                id_ticket = linha.split("**")[1].strip()
            elif linha.startswith("Atendente Atual:"):
                atendente_atual = linha.replace("Atendente Atual:", "").strip()
            elif linha.startswith("AIID:"):
                aiid = linha.split("**")[1].strip() if "**" in linha else linha.replace("AIID:", "").strip()

        if not id_ticket or not atendente_atual or not aiid:
            return

        # Verifica se o autor da mensagem é o solicitante do ticket (baseado no nome da thread)
        user_id = message.channel.name.split("-")[-1]
        try:
            solicitante = message.guild.get_member(int(user_id))
        except:
            solicitante = None

        # Detecta se há anexos (imagens, vídeos, etc.)
        midia_detectada = False
        if message.attachments:
            tipos_validos = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.mp4', '.mov', '.avi')
            for att in message.attachments:
                if any(att.filename.lower().endswith(ext) for ext in tipos_validos):
                    midia_detectada = True
                    break

        # Se o atendente atual é o bot
        if atendente_atual == message.guild.me.mention or atendente_atual == message.guild.me.name:
            if solicitante and message.author == solicitante:
                # Mensagem é do solicitante → enviar pra IA
                async with message.channel.typing():
                    conteudo = message.content
                    if midia_detectada:
                        conteudo += "\n[O usuário anexou uma mídia, pergunte se tem mais alguma coisa a enviar.]"
                    msg_ai = await response_ai_chat(aiid, conteudo)
                    await message.reply(msg_ai)
                return
            else:
                # Mensagem é de outro usuário (staff assumindo)
                novo_atendente = message.author.mention

                # Atualiza o embed
                novo_desc = ""
                for linha in linhas:
                    if linha.startswith("Atendente Atual:"):
                        novo_desc += f"Atendente Atual: {novo_atendente}\n"
                    else:
                        novo_desc += linha + "\n"

                embed.description = novo_desc.strip()
                await embed_msg.edit(embed=embed)

                await message.channel.send( Res.trad_nada(str="message_assumir_atendimento").format(novo_atendente) )
                return
        else:
            # Se já há atendente humano, ignora o comportamento automático
            return

















    @tasks.loop(minutes=2)
    async def check_inactive_channels(self):
        for guild in self.client.guilds:
            # Verifica canais e threads
            for channel in guild.text_channels:
                # --------------------------
                # PARTE 1 – Threads ativas
                # --------------------------
                for thread in channel.threads:
                    if thread.archived or not re.match(r"^[^┃]+┃\w+-\d+$", thread.name):
                        continue

                    try:
                        last_message = await thread.fetch_message(thread.last_message_id) if thread.last_message_id else None
                    except:
                        last_message = None
                    if not last_message:
                        continue

                    # Verifica tempo desde a última mensagem
                    time_diff = datetime.now(timezone.utc) - last_message.created_at
                    if time_diff <= timedelta(hours=48): #hours=48
                        continue

                    # Extrai o ID do solicitante a partir do nome da thread
                    match = re.search(r"-(\d+)$", thread.name)
                    if not match:
                        continue
                    solicitante = int(match.group(1))

                    # Pega a primeira mensagem (embed original)
                    first_message = None
                    async for msg in thread.history(limit=1, oldest_first=True):
                        first_message = msg
                        break

                    responsavel_role_id = None
                    atendimento_id = None
                    if first_message and first_message.embeds:
                        embed = first_message.embeds[0]
                        description = embed.description
                        if description:
                            responsavel_match = re.search(r"Responsavel: <@&(\d+)>", description)
                            atendimento_match = re.search(r"ID: \*\*([\w-]+)\*\*", description)
                            responsavel_role_id = int(responsavel_match.group(1)) if responsavel_match else None
                            atendimento_id = atendimento_match.group(1) if atendimento_match else None

                    # Se o bot foi o último a falar, encerra o ticket
                    async for message in thread.history(limit=1):
                        if message.author == self.client.user:
                            await thread.send(Res.trad_nada(str="mensagem_fechamento_ticket"))
                            await asyncio.sleep(5)
                            usuario = await self.client.fetch_user(solicitante)
                            await encerrar_thread(thread, guild, usuario)
                            try:
                                resposta = discord.Embed(
                                    colour=discord.Color.from_str('#f4de77'),
                                    description=Res.trad_nada(str="mensagem_fechamento_ticket_embed_description").format(atendimento_id)
                                )
                                resposta.set_thumbnail(url="https://i.imgur.com/ixqtABY.png")
                                resposta.set_footer(text=Res.trad_nada(str="message_encerrar_ticket_embed_footer"))
                                await usuario.send(embed=resposta)
                            except discord.Forbidden:
                                print(f"Não foi possível enviar mensagem para {solicitante}")
                            except Exception as e:
                                print(f"Erro ao enviar mensagem para {solicitante}: {e}")
                            continue

                        # Envia aviso de inatividade
                        if last_message.author.id != solicitante:
                            await thread.send(Res.trad_nada(str="mensagem_para_usuario_inativo").format(solicitante))
                        else:
                            await thread.send(Res.trad_nada(str="mensagem_para_staff_inativo").format(responsavel_role_id))



















    #COMANDO ABRIR ATENDIMENTO MENU
    async def abrirticketmenu(self, interaction: discord.Interaction, membro: discord.Member):
        print(f"Usuário: {interaction.user.name} usou Abrir Ticket")
        await interaction.response.defer(ephemeral=True)

        idatendimento = gerar_id_unica()
        tipoticket = "Outros Motivos"

        # Define os dados conforme o servidor
        if interaction.guild.id == id_servidor_bh:
            staff = id_cargo_atendente
            canal_atendimento = interaction.guild.get_channel(id_atendimento_principal)
        elif interaction.guild.id == id_servidor_tribunal:
            staff = id_cargo_tribunal
            canal_atendimento = interaction.guild.get_channel(id_atendimento_tribunal)
        else:
            await interaction.followup.send(ephemeral=True, content=Res.trad_nada(str="message_error_onlyBHTR"))
            return

        # Cria embed no mesmo padrão do CreateTicket
        embedticket = discord.Embed(
            colour=discord.Color.from_str('#f4de77'),
            description=( f"Atendimento: **{tipoticket}**\n" f"Responsável: <@&{staff}>\n" f"ID: **{idatendimento}**\n" f"Atendente Atual: {interaction.user.mention}\n" f"AIID: 0" )
        )
        embedticket.set_thumbnail(url="https://i.imgur.com/ixqtABY.png")
        embedticket.set_footer(text="Use o botão Finalizar Atendimento para encerrar seu atendimento!")

        # Cria a thread no canal de atendimento
        nome_thread = f"🦊┃{membro.name.lower().replace(' ', '-')}-{membro.id}"
        thread = await canal_atendimento.create_thread( name=nome_thread, type=discord.ChannelType.private_thread, invitable=False )

        # Envia mensagem de confirmação para quem abriu
        view = discord.ui.View()
        btn = discord.ui.Button( style=discord.ButtonStyle.gray, label=f"Ticket de {membro.name}", url=f"https://discord.com/channels/{interaction.guild.id}/{thread.id}" )
        view.add_item(btn)
        await interaction.followup.send( content=f"<:BH_Braix_Happy4:1154338634011521054> Ticket criado com sucesso! 🎉", view=view )

        # Mensagens iniciais no ticket
        await thread.send(f"Avisando: {membro.mention} e notificando <@&{staff}>")
        await asyncio.sleep(0.5)
        await thread.purge(limit=1)
        await thread.send(embed=embedticket, view=FinalizarTicket())
        await thread.send(f"💛 Este ticket foi aberto pelo administrador {interaction.user.mention} para realizar um atendimento exclusivo ao membro {membro.mention}, kyu~!")

















    #GRUPO PAINEIS DE ATENDIMENTO DO BOT 
    painel=app_commands.Group(name="painel",description="Comandos de paineis de atendimento do bot.")












        #PAINEL DE SUPORTE DO BRAIXEN'S HOUSE
    @painel.command(name = 'suporte-bh', description='🦊⠂Crie um Menu para atendimento de suporte')
    @commands.has_permissions(manage_guild=True)
    async def suportebh(self,interaction: discord.Interaction):
        print (f"Usuario: {interaction.user.name} usou painel suporte")
        embed1 = discord.Embed(
            colour=discord.Color.yellow(),
            title="Atendimento Braixen's House",
            description="Seja bem-vindo(a) a nossa **seção de ajuda** do **Braixen's House.** \n \nAqui você pode tirar dúvidas, pedir ajuda para alguns problemas, solicitar cargos, informar sobre problemas de acesso, sugestões de mudanças entre outros basta selecionar a opção desejada."
        )
        embed1.set_image(url="https://cdn.discordapp.com/attachments/1067789510097768528/1146086873501028513/atendimento.png")
        if interaction.user.id == donoid:
            await interaction.response.send_message("Painel criado",ephemeral=True)
            await interaction.channel.send(embed=embed1,view=DropdownSuporte()) 
        else:await interaction.response.send_message(mensagemerro,ephemeral=True)












        #PAINEL DO TRIBUNAL DO BRAIXEN'S HOUSE
    @painel.command(name = 'tribunal', description='🦊⠂Crie um Menu para atendimento do tribunal.')
    @commands.has_permissions(manage_guild=True)
    async def tribunalbh(self,interaction: discord.Interaction):
        print (f"Usuario: {interaction.user.name} usou painel tribunal")
        embed3 = discord.Embed(
            colour=discord.Color.yellow(),
            title="Tribunal Braixen's House",
            description="Seja bem-vindo(a) ao **Tribunal** do **Braixen's House.** \n \nAqui você pode verificar e contestar banimentos e avisos que aconteceram no Braixen's House.\n\n**Atenção** não abra ticket sem motivo, caso contrario poderemos ignorar sua solicitação."
        )
        #imagem do meu embed
        embed3.set_image(url="https://cdn.discordapp.com/attachments/1067789510097768528/1146086949057208410/tribunal.png")
        if interaction.user.id == donoid:
            await interaction.response.send_message("Painel criado",ephemeral=True)
            await interaction.channel.send(embed=embed3,view=DropdownTribunal()) 
        else:await interaction.response.send_message(mensagemerro,ephemeral=True)






























    #GRUPO DE ATENDIMENTO DO BOT 
    atendi=app_commands.Group(name="atendimento",description="Comandos de paineis de atendimento do bot.")












    #COMANDO PARA FECHAR UM TICKET
    #esse cara manda um texto e manda junto o botão de fechar ticket 
    @atendi.command(name="fechar",description='📞⠂Feche um atendimento.')
    async def fecharticket(self,interaction: discord.Interaction):
        print (f"Usuario: {interaction.user.name} usou fecharticket")
        mod = interaction.guild.get_role(id_cargo_atendente)
        mod2 = interaction.guild.get_role(id_cargo_tribunal)
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.user.roles or mod2 in interaction.user.roles:
            await interaction.response.send_message("<:BraixThink:969396723631939594> **Você deseja mesmo Encerrar seu atendimento?")
            await asyncio.sleep(1.5)
            await interaction.followup.send("Caso sim, use o botão abaixo.",view=DeleteTicket())
        else:
            await interaction.response.send_message(mensagemerro,ephemeral=True)














        #COMANDO DE ENVIO DE OBRIGADO
        #esse aqui manda um obrigado ao membro da equipe do servidor, reconhece automaticamente com base na id no canal.
    @atendi.command(name='encerrar', description='📞⠂Encerre um atendimento.')
    async def encerrar(self,interaction: discord.Interaction):
        print (f"Usuario: {interaction.user.name} usou obg atendimento")
        mod = interaction.guild.get_role(id_cargo_atendente)
        mod2 = interaction.guild.get_role(id_cargo_tribunal)
        membro_id = interaction.channel.name.split('-')[-1]
        membro = interaction.guild.get_member(int(membro_id))
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.user.roles or mod2 in interaction.user.roles:
            await interaction.response.send_message("enviando mensagem...",ephemeral=True)
            async with interaction.channel.typing():
                    await asyncio.sleep(1.5)
            await interaction.channel.send(f"Olá novamente {membro.mention}!!!")
            async with interaction.channel.typing():
                    await asyncio.sleep(2)
            await interaction.channel.send(f"Parece que seu atendimento está chegando ao fim.")
            async with interaction.channel.typing():
                    await asyncio.sleep(2)
            await interaction.channel.send(f"O *Braixen's House* agradece o contato e esperamos que você não tenha ficado com nenhuma dúvida sobre sua solicitação. <:BraixHappy2:988776437790158918>")
            async with interaction.channel.typing():
                    await asyncio.sleep(2)
            await interaction.channel.send(f"Você pode **avaliar o seu atendimento** usando o comando </atendimento avaliar:1138614448840511577>.")
            async with interaction.channel.typing():
                    await asyncio.sleep(2)
            await interaction.channel.send(f"Por favor use o **comando** </atendimento fechar:1138614448840511577> para **finalizar seu atendimento**")
        else:
            await interaction.response.send_message(mensagemerro,ephemeral=True)













        #COMANDO PARA ADICIONAR ALGUEM A ALGUM ATENDIMENTO
    #esse aqui adiciona um novo membro ao atendimento atual e notifica no chat que foi adicionado
    @atendi.command(name="adicionar",description='📞⠂Adicione um membro ao atendimento.')
    async def adicionar(self,interaction: discord.Interaction):
        print (f"Usuario: {interaction.user.name} usou add atendimento")
        mod = interaction.guild.get_role(id_cargo_atendente)
        mod2 = interaction.guild.get_role(id_cargo_tribunal)
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.user.roles or mod2 in interaction.user.roles:
            await interaction.response.send_message(Res.trad_nada(str="message_add_user_ticket"),delete_after=120,view=DropdownMembro(interaction, action='adicionar'))
        else:
            await interaction.response.send_message(Res.trad_nada(str="message_erro_onlyStaff/Solicitante"),delete_after=20,ephemeral=True)









                    #COMANDO PARA REMOVER ALGUEM A ALGUM ATENDIMENTO
    @atendi.command(name="remover",description='📞⠂Remove um membro do atendimento.')
    async def remover(self,interaction: discord.Interaction):
        print (f"Usuario: {interaction.user.name} usou rem atendimento")
        mod = interaction.guild.get_role(id_cargo_atendente)
        mod2 = interaction.guild.get_role(id_cargo_tribunal)
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.user.roles or mod2 in interaction.user.roles:
            await interaction.response.send_message(Res.trad_nada(str="message_rem_user_ticket"),delete_after=120,view=DropdownMembro(interaction, action='remover'))
        else:
            await interaction.response.send_message(Res.trad_nada(str="message_erro_onlyStaff/Solicitante"),delete_after=20,ephemeral=True)

     











                #COMANDO PARA AVALIAR O ATENDIMENTO
            #esse comando permite que o membro envie uma avaliação sobre o atendimento, o membro pode escolher o staff, indicar a nota, e adicionar um comentario, as avaliações são registradas no canal de avaliação.
    @atendi.command(name="avaliar",description='📞⠂Avalie seu atendimento na nossa comunidade.')
    @app_commands.describe(staff="informe um membro da staff para avaliar",nota="selecione uma nota para o staff",comentario="escreva um comentario adicional.")
    @app_commands.choices(nota=[app_commands.Choice(name="1", value="1"),app_commands.Choice(name="2", value="2"),app_commands.Choice(name="3", value="3"),app_commands.Choice(name="4", value="4"),app_commands.Choice(name="5", value="5"),])
    async def avaliar(self,interaction: discord.Interaction,staff: discord.Member, nota:app_commands.Choice[str],comentario:str):
        print (f"Usuario: {interaction.user.name} usou avaliar atendimento")
        canal_avaliacao = interaction.guild.get_channel(id_canal_avaliacao)
        if (nota.value == '1'):
            estrelas = "🦊"
        elif (nota.value == '2'):
            estrelas = "🦊🦊"
        elif (nota.value == '3'):
            estrelas = "🦊🦊🦊"
        elif (nota.value == '4'):
            estrelas = "🦊🦊🦊🦊"
        elif (nota.value == '5'):
            estrelas = "🦊🦊🦊🦊🦊"
    
        resposta = discord.Embed(
                colour=discord.Color.yellow()
            )
        resposta.set_thumbnail(url=staff.avatar.url)
        resposta.add_field(name="```🦊``` Staff", value=f"```{staff.name}#{staff.discriminator}```", inline=True)
        resposta.add_field(name="```⭐``` Nota", value=f"```{estrelas}```", inline=True)
        resposta.add_field(name="```🗨️``` comentário", value=f"```{comentario}```", inline=False)
        resposta.set_footer(text=f"avaliação enviada por {interaction.user.name}#{interaction.user.discriminator}")
        await canal_avaliacao.send(embed=resposta)
        await interaction.response.send_message("Recebemos sua avaliação ebaaa <:BraixHappy2:988776437790158918> muito obrigado viu <:Braixen_Kyu:984628502450016286>",ephemeral=True)

    
    













    
 #COMANDO PARA A STAFF ABRIR UM ATENDIMENTO
    @atendi.command(name="abrir-atendimento",description='📞⠂Abra um atendimento Imediatamente.')
    @app_commands.describe(membro="Indique um membro da comunidade.")
    async def abrirticketstaff(self,interaction: discord.Interaction, membro : discord.Member):
        print (f"Usuario: {interaction.user.name} usou abrirticketstaff")
        mod = interaction.guild.get_role(id_cargo_atendente)
        mod2 = interaction.guild.get_role(id_cargo_tribunal)
        if mod in interaction.user.roles or mod2 in interaction.user.roles:
            await self.abrirticketmenu(interaction,membro)
        else:
            await interaction.response.send_message(Res.trad_nada( str="message_erro_onlyStaffBH"),delete_after=20,ephemeral=True)










async def setup(client:commands.Bot) -> None:
  await client.add_cog(atendimento(client))
