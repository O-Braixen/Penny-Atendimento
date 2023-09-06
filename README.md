# Braixen-Atendimento

![bot image](img/Braixen%20Atendimento.jpg)


**ESSE REPOSITORIO FOI FECHADO POIS O BOT DE ATENDIMENTO FOI MIGRADO PARA UM NOVO MODELO COM COGS, CONHEÇA O [BRIX](https://github.com/O-Braixen/Brix).**


codigo em Python do Bot de atendimento do Braixen's House

Esse codigo foi desenvolvido a partir do curso do Dominado o discord do [Youtuber Dune](https://www.youtube.com/@DuneDiscord) e modificado para atender aos requisitos da comunidade [Braixen's House](https://discord.gg/ZRHwWydQFu)

Todas os comandos estão com comentarios e explicados para facil modificação e os arquivos de dependencias e de hospedagem na squarecloud estão adicionadas ao repositorio. divirta-se

**Segue as especificações desse codigo**

 - 3 Paineis de Dropdown (2 para um servidor e 1 para um segundo servidor);
 - Suporte aos paineis serem persistentes;
 - Adicionado suporte para salvar chat ao fechar ticket
 - Suporte a context_menu para alguns comandos
 - suporte a .env adicionado

**Lista dos comandos de context menu**
 - Avatar
 - Usuario info
 - Abrir Ticket

**Lista dos comandos**

- /painel_suporte
- /painel_servicos
- /painel_tribunal
- /fecharticket
- /atendimento_obrigado
- /atendimento_adicionar
- /atendimento_remover
- /say
- /ping
- /bot_info
- /user_banir
- /user_cargo_adicionar
- /user_cargo_remover
- /user_info
- /user_avatar
- /cargo
- /canal_delete
- /limpar_chat

**Variaveis exigidas**

- donoid
- id_cargo_atendente
- id_cargo_tribunal
- id_categoria_staff
- id_categoria_tribunal
- id_servidor_bh
- id_servidor_tribunal
- id_canal_logs_bh
- id_canal_logs_tri
- token_bot (Via .env)
