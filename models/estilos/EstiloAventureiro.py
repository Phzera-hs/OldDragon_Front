import models.Personagem as P
import utils.Rolagem_Dados as Rd

class Estilo_Aventureiro(P.Personagem):
    def __init__(self, nome, raca):
        super().__init__(nome, raca)
        self.valores = self.Vetorizacao_Rolagem()

    def Vetorizacao_Rolagem(self):
        valores = []
        for i in range(6):
            soma = 0
            for j in range(3):
                d6 = Rd.Rola_Dados.rolando_d6()
                soma += d6
            valores.append(soma)
        return valores

    # Remover o método Definindo_Atributos que usa console