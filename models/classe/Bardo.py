import models.Classe as C

class Bardo(C.Classe):
    def __init__(self):
        habilidades_iniciais = [
            "Inspiração", 
            "Performance", 
            "Persuasão",
            "Conhecimento Geral"
        ]
        super().__init__("Bardo", dado_vida=6, habilidades_iniciais=habilidades_iniciais)
        self.bonus_inspiracao = 1
        
    def inspirar_aliados(self):
        return f"Inspira aliados com +{self.bonus_inspiracao} em testes"
        
    def subir_nivel(self, constituicao):
        super().subir_nivel(constituicao)
        if self.nivel % 4 == 0:
            self.bonus_inspiracao += 1
        return self.pontos_de_vida