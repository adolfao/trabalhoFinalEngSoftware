class Professor:
    def __init__(self, id_prof: int, nome: str, disponibilidade: dict, preferencias: list = None):
        self.id_prof = id_prof
        self.nome = nome
        self.disponibilidade = disponibilidade  # {"Segunda": ["M1", "M2", ...]}
        self.preferencias = preferencias or []  # dias preferidos: ["Segunda", "Quarta"]

    def disponivel_em(self, dia: str, horario: str) -> bool:
        return horario in self.disponibilidade.get(dia, [])
