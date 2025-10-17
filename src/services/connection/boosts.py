import os
import json

# Definindo o caminho do arquivo JSON
BOOSTS_FILE_PATH = os.path.join('src/services/caches', 'boosts.json') #'boosts.json'

# Verifica se o arquivo existe, senão, cria um novo arquivo com um dicionário vazio
if not os.path.exists(BOOSTS_FILE_PATH):
    with open(BOOSTS_FILE_PATH, 'w') as file:
        json.dump({}, file)

# Função para ler os dados dos boosts do arquivo JSON
def read_json():
    with open(BOOSTS_FILE_PATH, 'r') as file:
        return json.load(file)

# Função para escrever os dados dos boosts no arquivo JSON
def write_json(data):
    with open(BOOSTS_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

async def changeBoost(user, boosts): 
    data = read_json()
    user_id_str = str(user.id)
    data[user_id_str] = {"boosts": boosts}
    write_json(data)
    return data[user_id_str]

async def addBoost(user): 
    user_id_str = str(user.id)
    data = read_json()
    if user_id_str not in data:
        data[user_id_str] = {"boosts": 1}
    else:
        data[user_id_str]["boosts"] += 1
    write_json(data)
    return data[user_id_str]["boosts"]

async def getBoosts(user):
    user_id_str = str(user.id)
    data = read_json()
    return data.get(user_id_str, {"boosts": 0})["boosts"]
