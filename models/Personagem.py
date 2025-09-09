import utils.Console_Utils

class Personagem():
    def __init__(self, nome, raca):
        self.nome = nome
        self.raca = raca
        self.classe = None 
        self.atributos = {
            "forca": 0,
            "destreza": 0,
            "constituicao": 0,
            "inteligencia": 0,
            "sabedoria": 0,
            "carisma": 0,
        }
        self.valores = []

    def escolher_classe(self, classe):
        self.classe = classe
        self.classe.rolar_pontos_de_vida(self.atributos["constituicao"])

    def aplicar_bonus_raca(self):
        for atributo, bonus in self.raca.modificadores.items():
            self.atributos[atributo] += bonus

    def Definindo_Atributos(self):
        atributos = list(self.atributos.keys())
        
        for atributo in atributos:
            while True:
                print(f"\nValores disponíveis: {self.valores}\n")
                valorUser = input(f"{atributo.capitalize()} = ")

                if valorUser.isdigit():
                    valor = int(valorUser)
                    if valor in self.valores:
                        self.atributos[atributo] = valor
                        self.valores.remove(valor)
                        print(f"{atributo.capitalize()} atribuído = {valor}")
                        break
                print(f"O valor '{valorUser}' não é válido.")

        self.aplicar_bonus_raca()

    def Mostrando_Jogador(self):
        utils.Console_Utils.limpar_tela()
        print("\n---- FICHA DO JOGADOR ----")
        print(f"Nome: {self.nome}")
        print(f"Raça: {self.raca.nome}")
        if self.classe:
            print(f"Classe: {self.classe.nome} (Nível {self.classe.nivel})")
            print(f"\tHabilidades de Classe: {', '.join(self.classe.habilidades)}")
            
            print(f"Pontos de Vida: {self.classe.pontos_de_vida}")
        if self.raca:
            print(f"Movimento: {self.raca.movimento}m")
            if(self.raca.infravisao > 0):
                print(f"Infravisão: {self.raca.infravisao}m")
            else:
                print(f"Infravisão: Não possui")
            print(f"Alinhamento: {self.raca.alinhamento}")
        print("\nATRIBUTOS:")
        for atributo, valor in self.atributos.items():
            barras = "█" * valor  # Barras cheias
            espacos = " " * (20 - valor)  # Espaços em branco
            print(f"{atributo.capitalize():12} |{barras}{espacos}| {valor}")