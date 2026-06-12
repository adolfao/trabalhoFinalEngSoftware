class Professor:
    def __init__(self, id_prof: int, nome: str, disponibilidade: dict, preferencias: list = None, semestre: str = "2026/1"):
        self.id_prof = id_prof
        self.nome = nome
        self.disponibilidade = disponibilidade
        self.preferencias = preferencias or []
        self.semestre = semestre

    def disponivel_em(self, dia: str, horario: str) -> bool:
        return horario in self.disponibilidade.get(dia, [])