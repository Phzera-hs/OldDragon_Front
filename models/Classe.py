import random

class Classe:
    def __init__(self, nome, dado_vida, habilidades_iniciais):
        self.nome = nome
        self.dado_vida = dado_vida
        self.habilidades = habilidades_iniciais
        self.nivel = 1
        self.pontos_de_vida = 0
        
    def rolar_pontos_de_vida(self, constituicao):
        import random
        bonus_constituicao = (constituicao - 10) // 2
        vida = random.randint(1, self.dado_vida) + bonus_constituicao
        self.pontos_de_vida = max(1, vida) 
        return self.pontos_de_vida
        
    def subir_nivel(self, constituicao):
        self.nivel += 1
        bonus_constituicao = (constituicao - 10) // 2
        novo_pv = random.randint(1, self.dado_vida) + bonus_constituicao
        self.pontos_de_vida += max(1, novo_pv)  
        return self.pontos_de_vida
        
    def __str__(self):
        return (f"Classe: {self.nome}\n"
                f"Nível: {self.nivel}\n"
                f"Dado de Vida: d{self.dado_vida}\n"
                f"Pontos de Vida: {self.pontos_de_vida}\n"
                f"Habilidades: {', '.join(self.habilidades)}")