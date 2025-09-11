import models.Raca as R

class Humano(R.Raca):
    def __init__(self, alinhamento="Neutro"):
        super().__init__("Humano", movimento=9, infravisao=0, alinhamento=alinhamento)
        for atributo in self.modificadores:
            self.modificadores[atributo] = 1
        self.habilidades = ["Aprendizado", "Adaptabilidade"]
        
    # REMOVIDO: Método Alinhamento() que usava input() - agora tratado no Flask