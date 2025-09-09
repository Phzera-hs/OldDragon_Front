import models.Raca as R


class Halfling(R.Raca):
    def __init__(self):
        super().__init__("Halfling", movimento=6, infravisao=0, alinhamento="Neutro")
        self.modificadores["carisma"] = 2
        self.modificadores["destreza"] = 1
        self.modificadores["sabedoria"] = 1
        self.habilidades = ["Furtivo","Destemido","Bons de Mira",
                            "Pequenos","Restrições"]
        
        
        
