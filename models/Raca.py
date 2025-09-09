class Raca:
    def __init__(self, nome, movimento, infravisao, alinhamento):
        self.nome = nome
        self.movimento = movimento
        self.infravisao = infravisao
        self.alinhamento = alinhamento
        self.modificadores = {
            "forca": 0,
            "destreza": 0,
            "constituicao": 0,
            "inteligencia": 0,
            "sabedoria": 0,
            "carisma": 0,
        }
        self.habilidades = []

    def aplicar_bonus(self, personagem):
        for atributo, bonus in self.modificadores.items():
            if hasattr(personagem, atributo):
                valor_atual = getattr(personagem, atributo)
                setattr(personagem, atributo, valor_atual + bonus)

    def __str__(self):
        return (f"Raça: {self.nome}\n"
                f"Movimento: {self.movimento}\n"
                f"Infravisão: {self.infravisao}\n"
                f"Alinhamento: {self.alinhamento}\n"
                f"Habilidades: {', '.join(self.habilidades)}")


        