import json
import os

CAMINHO_ARQUIVO = os.path.join('src/services/caches','list_autokick.json') #'role_id.json'


def carregar_banlist():
    if not os.path.exists(CAMINHO_ARQUIVO):
        with open(CAMINHO_ARQUIVO, "w") as f:
            json.dump([], f)
    with open(CAMINHO_ARQUIVO, "r") as f:
        return json.load(f)

def salvar_banlist(lista):
    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(lista, f, indent=4)

def usuario_na_banlist(lista, user_id):
    return any(entry["id"] == user_id for entry in lista)

def remover_usuario_da_banlist(lista, user_id):
    return [entry for entry in lista if entry["id"] != user_id]
