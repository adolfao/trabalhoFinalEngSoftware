from modelos.disciplina import Disciplina

class FabricaDisciplina:
    @staticmethod
    def criar_disciplina(codigo: str, nome: str, periodo: int, carga_horaria: int) -> Disciplina:
        if carga_horaria not in [30, 60, 90]:
            raise ValueError("Carga horária inválida! Use 30, 60 ou 90.")
        if periodo <= 0:
            raise ValueError("O período deve ser um número positivo.")
        return Disciplina(codigo, nome, periodo, carga_horaria)