import models.Classe as C

class Mago(C.Classe):
    def __init__(self):
        habilidades_iniciais = [
            "Magia Arcana", 
            "Conhecimento Mágico", 
            "Identificar Magia",
            "Preparar Feitiços"
        ]
        super().__init__("Mago", dado_vida=4, habilidades_iniciais=habilidades_iniciais)
        self.magias_conhecidas = 3
        self.magias_preparadas = 1
        
    def preparar_magia(self):
        return f"O mago prepara {self.magias_preparadas} magia(s) para o dia"
        
    def subir_nivel(self, constituicao):
        super().subir_nivel(constituicao)
        if self.nivel % 2 == 0:  
            self.magias_conhecidas += 1
        if self.nivel % 3 == 0: 
            self.magias_preparadas += 1
        return self.pontos_de_vida