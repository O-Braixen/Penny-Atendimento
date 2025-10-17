import os,json



respostas = {}
# Listar arquivos na pasta
for arquivo in os.listdir("src/core/responses"):
    caminho_arquivo = os.path.join("src/core/responses", arquivo)

    # Verificar se é um arquivo JSON
    if os.path.isfile(caminho_arquivo) and arquivo.endswith(".json"):
        # Extrair o idioma do nome do arquivo (assumindo que os nomes têm um padrão)
        idioma = arquivo.split(".")[0]

        # Carregar o arquivo JSON no dicionário respostas
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            respostas[idioma] = json.load(file)


class Res:
  def trad_nada(str):
    res = respostas['pt-BR'].get(f"{str}")
    return res  
  
    