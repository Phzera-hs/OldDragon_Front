import models.Personagem as P
import utils.Rolagem_Dados as Rd

class Estilo_Classico(P.Personagem):
    def __init__(self, nome, raca):
        super().__init__(nome, raca)
        self.atributos["forca"] = Rd.Rola_Dados.rolagem_atributo()
        self.atributos["destreza"] = Rd.Rola_Dados.rolagem_atributo()
        self.atributos["constituicao"] = Rd.Rola_Dados.rolagem_atributo()
        self.atributos["inteligencia"] = Rd.Rola_Dados.rolagem_atributo()
        self.atributos["sabedoria"] = Rd.Rola_Dados.rolagem_atributo()
        self.atributos["carisma"] = Rd.Rola_Dados.rolagem_atributo()

        self.aplicar_bonus_raca() 