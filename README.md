# Penny - A atendente multi-uso

![bot image](img/Penny_avatar.jpg)


Codigo em Python do Bot de interação e atendimento do Braixen's House com suporte a Cogs

**AVISO**: Esse repositorio antes se chamava Brix, pois ele antes era um bot de atendimento, mas agora se tornou um bot multi tarefas, e esse repositorio foi trocado para Penny (atendente da BH) nas proximas semanas estarei revisando 100% desse codigo, adicionando também recurso de copiador de chat e acompanhante de boost.

Esse codigo foi desenvolvido e aprimorado a partir do [antigo Braixen Atendimento](https://github.com/O-Braixen/Braixen-Atendimento) usando os conhecimentos do curso do Dominado o discord do [Youtuber Dune](https://www.youtube.com/@DuneDiscord) e modificado para atender aos requisitos da comunidade [Braixen's House](https://discord.gg/ZRHwWydQFu)

Todas os comandos estão com comentarios e explicados para facil modificação e os arquivos de dependencias e de hospedagem na squarecloud estão adicionadas ao repositorio. divirta-se

**Segue as especificações desse codigo**

 - 3 Paineis de Dropdown (2 para um servidor e 1 para um segundo servidor);
 - Suporte aos paineis serem persistentes;
 - Adicionado suporte para salvar chat ao fechar ticket
 - Suporte a **context_menu** para alguns comandos
 - suporte a .env adicionado
 - **codigo em cog facil de receber updates**
 - varios comandos voltados para usuarios
 - comando de avaliação de atendimento **novo**
 - comando de abertura de ticket de entrevista **novo**

**Lista dos comandos de context menu**
 - Usuario Avatar
 - Usuario Info
 - Usuario Banner
 - Usuario Abraço

**Lista dos comandos**

- /owner say
- /owner listar
- /owner sair
- /owner bot-name
- /owner bot-avatar
---------------------------
- /bot ping
- /bot info
- /bot help
---------------------------
- /usuario avatar
- /usuario info
- /usuario abraçar
- /usuario banner
- /usuario atacar
- /usuario carinho
- /usuario cafuné
- /usuario afk
---------------------------
- /servidor icone
- /servidor banner
- /servidor splash
- /servidor info
---------------------------
- /admin banir 
- /admin desbanir 
- /admin kick 
---------------------------
- /chat deletar 
- /chat limpar 
- /chat criar 
- /chat info
---------------------------
- /canal deletar 
- /canal limpar 
- /canal criar 
- /canal info
---------------------------
- /cargo adicionar 
- /cargo remover 
- /cargo trocar 
- /cargo info
---------------------------
- /painel suporte-bh
- /painel servicos-bh
- /painel tribunal
---------------------------
- /atendimento fechar
- /atendimento encerrar
- /atendimento adicionar
- /atendimento remover
- /atendimento avaliar
- /atendimento entrevista

**Instruções de instalação**

Caso você rode na Squarecloud (onde esse codigo foi planejado) basta editar todo o arquivo exemplo.env e ao final deve renomea-lo para apenas .env e compacte tudo e envie para a squarecloud.

Caso queira rodar localmente recomendo o uso do VScode e para instalar os requisitos use *pip install -r requirements.txt* para que o sistema instale todos os requisitos antes de iniciar seu bot.


**Variaveis exigidas**

- SUA ID em DONO_ID
- Token do seu bot em DISCORD_TOKEN
- Token da square em square_token
- Id do seu bot na square em square_idaplication
- todas as outras variaveis de cargos e canais para funcionamento da parte de atendimento.
