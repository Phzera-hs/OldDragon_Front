import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "personagens.json")

# garante que a pasta 'data' exista
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def carregar_personagens():
    if not os.path.exists(DB_PATH):
        return []  # banco vazio
    with open(DB_PATH, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def salvar_personagem(nova_ficha):
    personagens = carregar_personagens()
    personagens.append(nova_ficha)
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(personagens, file, ensure_ascii=False, indent=2)
