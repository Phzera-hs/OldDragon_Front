import models.Raca as R


class Anao(R.Raca):
    def __init__(self):
        super().__init__("Anão", movimento = 6, infravisao = 18, alinhamento = "Ordem")
        self.modificadores["constituicao"] = 2
        self.modificadores["forca"] = 2
        self.habilidades = ["Mineradores", "Vigoroso", "Armas Grandes", "Inimigos"]