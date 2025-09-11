import models.Personagem as P
import utils.Rolagem_Dados as Rd

class Estilo_Heroico(P.Personagem):
    def __init__(self, nome, raca):
        super().__init__(nome, raca)
        self.valores = self.TiraMenor()

    def TiraMenor(self):
        valores = []

        for qntd_roll in range(6):
            d6 = []
            soma = 0
            for dados_in_roll in range(4):
                dados_in_roll = Rd.Rola_Dados.rolando_d6()
                d6.append(dados_in_roll)
                soma += dados_in_roll

            d6 = sorted(d6, key=None, reverse=False)
            menor = d6.pop(0)
            soma -= menor
            valores.append(soma)

        return valores

    # Remover o método Definindo_Atributos que usa console