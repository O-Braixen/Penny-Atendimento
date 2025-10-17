import json
import os

ROLE_ID_FILE_PATH = os.path.join('src/services/caches', 'role_id.json') #'role_id.json'

# Verifica se o arquivo existe, senão, cria um novo arquivo com dados vazios
if not os.path.exists(ROLE_ID_FILE_PATH):
    with open(ROLE_ID_FILE_PATH, 'w') as file:
        json.dump({"role_id": None}, file)

# Função para ler o ID do canal do arquivo JSON
def get_role_id():
    with open(ROLE_ID_FILE_PATH, 'r') as file:
        data = json.load(file)
    return data.get("role_id")

# Função para escrever o ID do canal no arquivo JSON
def set_role_id(role_id):
    with open(ROLE_ID_FILE_PATH, 'w') as file:
        json.dump({"role_id": role_id}, file, indent=4)