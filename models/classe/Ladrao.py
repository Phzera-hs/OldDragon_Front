import models.Classe as C

class Ladrao(C.Classe):
    def __init__(self):
        habilidades_iniciais = [
            "Furtividade", 
            "Armadilhas", 
            "Punga",
            "Escalar Superfícies"
        ]
        super().__init__("Ladrão", dado_vida=6, habilidades_iniciais=habilidades_iniciais)
        self.bonus_ataque_furtivo = 1
        
    def ataque_furtivo(self):
        return f"Ataque furtivo com +{self.bonus_ataque_furtivo}d6 de dano extra"
        
    def subir_nivel(self, constituicao):
        super().subir_nivel(constituicao)
        if self.nivel % 3 == 0:
            self.bonus_ataque_furtivo += 1
        return self.pontos_de_vida