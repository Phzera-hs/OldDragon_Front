import models.Personagem as P
import utils.Rolagem_Dados as Rd
import utils.Console_Utils as Cons
import time


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