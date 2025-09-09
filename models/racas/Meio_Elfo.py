import models.Raca as R


class Meio_Elfo(R.Raca):
    def __init__(self):
        super().__init__("Meio-Elfo", movimento=9, infravisao=9, alinhamento="Caos")
        self.modificadores["destreza"] = 3
        self.modificadores["inteligencia"] = 1
        self.habilidades = ["Aprendizado","Gracioso e Vigoroso",
                            "Idioma Extra","Imunidades"]
        
