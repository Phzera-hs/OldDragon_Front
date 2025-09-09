import models.Raca as R


class Elfo(R.Raca):
    def __init__(self):
        super().__init__("Elfo", movimento=9, infravisao=18, alinhamento="Neutro")
        self.modificadores["constituicao"] = 2
        self.modificadores["inteligencia"] = 2
        self.habilidades = ["Percepção Natural","Graciosos",
                            "Treinamento Racial","Imunidades"]