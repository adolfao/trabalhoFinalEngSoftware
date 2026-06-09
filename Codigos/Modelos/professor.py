class Professor:
    def __init__(self, id_prof: int, nome: str, disponibilidade: dict):
        self.id_prof = id_prof
        self.nome = nome
        self.disponibilidade = disponibilidade  # Ex: {'segunda': ['07:00', '09:10']}