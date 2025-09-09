import models.Personagem as P
import utils.Rolagem_Dados as Rd
import utils.Console_Utils as Cons
import time

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

            d6 = sorted(d6, key = None, reverse=False)
            menor = d6.pop(0)
            soma -= menor
            valores.append(soma)

        return valores

    def Definindo_Atributos(self):
        atributos = list(self.atributos.keys())
        
        for atributo in atributos:
            while True:
                Cons.limpar_tela()
                print(f"\nValores disponíveis: {self.valores}\n")
                valorUser = input(f"{atributo.capitalize()} = ")

                if valorUser.isdigit():
                    valor = int(valorUser)
                    if valor in self.valores:
                        self.atributos[atributo] = valor
                        self.valores.remove(valor)
                        print(f"{atributo.capitalize()} atribuído = {valor}")
                        time.sleep(0.8)                
                        break
                print(f"O valor '{valorUser}' não é válido.")
                time.sleep(0.8)

        self.aplicar_bonus_raca() 