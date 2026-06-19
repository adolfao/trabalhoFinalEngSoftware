class Disciplina:
    def __init__(self, codigo: str, nome: str, periodo: int, carga_horaria: int, turma: str = "Unica"):
        self.codigo = codigo
        self.nome = nome
        self.periodo = periodo
        self.carga_horaria = carga_horaria
        self.turma = turma