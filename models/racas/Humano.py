import models.Raca as R
import utils.Console_Utils

class Humano(R.Raca):
    def __init__(self):
        alinhamento = self.Alinhamento()
        super().__init__("Humano", movimento=9, infravisao=0, alinhamento=alinhamento)
        for atributo in self.modificadores:
            self.modificadores[atributo] = 1
        self.habilidades = ["Aprendizado", "Adaptabilidade"]
        
        
    def Alinhamento(self):
        while True:
            print("\nDefina o seu alinhamento:")
            print("Neutro - 1")
            print("Ordem - 2 ")
            print("Caos - 3 ")
            
            alinhamento_opcao = input("Opção: ")
            
            if (alinhamento_opcao == "1"):
                return "Neutro"
            elif (alinhamento_opcao == "2"):
                return "Ordem"
            elif (alinhamento_opcao == "3"):
                return"Caos"
            else:
                print(f"Valor {alinhamento_opcao} incorreto!")
        