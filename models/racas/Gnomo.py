import models.Raca as R


class Gnomo(R.Raca):
    def __init__(self):
        super().__init__("Gnomo", movimento=6, infravisao=18, alinhamento="Neutro")
        self.modificadores["carisma"] = 3
        self.modificadores["destreza"] = 1
        self.habilidades = ["Avaliadores", "Sagazes e Vigorosos", "Restrições"]