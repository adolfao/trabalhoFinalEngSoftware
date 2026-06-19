from modelos.disciplina import Disciplina

class FabricaDisciplina:
    @staticmethod
    def criar_disciplina(codigo: str, nome: str, periodo: int, carga_horaria: int, turma: str = "Unica") -> Disciplina:
        if carga_horaria not in [30, 60, 90]:
            raise ValueError("Carga horaria invalida! Use 30, 60 ou 90.")
        if periodo <= 0:
            raise ValueError("O periodo deve ser um numero positivo.")
        if not turma.strip():
            raise ValueError("A turma nao pode ser vazia.")
        return Disciplina(codigo, nome, periodo, carga_horaria, turma)