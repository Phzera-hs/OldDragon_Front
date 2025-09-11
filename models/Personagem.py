from abc import ABC, abstractmethod
import json

class Personagem(ABC):
    def __init__(self, nome, raca):
        self.nome = nome
        self.raca = raca
        self.classe = None 
        self.atributos = {
            "forca": 0,
            "destreza": 0,
            "constituicao": 0,
            "inteligencia": 0,
            "sabedoria": 0,
            "carisma": 0,
        }
        self.valores = []

    def escolher_classe(self, classe):
        self.classe = classe
        self.classe.rolar_pontos_de_vida(self.atributos["constituicao"])

    def aplicar_bonus_raca(self):
        for atributo, bonus in self.raca.modificadores.items():
            self.atributos[atributo] += bonus

    def get_ficha_dict(self):
        """Retorna um dicionário com os dados da ficha para a sessão"""
        return {
            'nome': self.nome,
            'raca': self.raca.nome,
            'classe': self.classe.nome if self.classe else None,
            'nivel': self.classe.nivel if self.classe else 1,
            'habilidades': self.classe.habilidades if self.classe else [],
            'pontos_vida': self.classe.pontos_de_vida if self.classe else 0,
            'movimento': self.raca.movimento,
            'infravisao': self.raca.infravisao,
            'alinhamento': self.raca.alinhamento,
            'atributos': self.atributos.copy(),  # Usar cópia para evitar referência
            'modificadores_raca': self.raca.modificadores.copy(),
        'habilidades_raca': self.raca.habilidades
    }

    def to_json(self):
        """Serializa o personagem para JSON"""
        return json.dumps(self.get_ficha_dict(), ensure_ascii=False, indent=2)

    def calcular_modificador(self, valor):
        """Calcula modificador de atributo baseado no valor"""
        return (valor - 10) // 2

    def get_modificadores(self):
        """Retorna dicionário com modificadores de todos os atributos"""
        return {atributo: self.calcular_modificador(valor) 
                for atributo, valor in self.atributos.items()}