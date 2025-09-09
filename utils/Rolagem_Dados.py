import random

class Rola_Dados():
    @staticmethod
    def rolando_d6():
        return random.randint(1, 6)
    
    @staticmethod
    def rolagem_atributo():
        soma = 0
        for i in range(3):
            dado = Rola_Dados.rolando_d6()
            soma += dado
        return soma