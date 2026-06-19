from Modelos.professor import Professor

class FabricaProfessor:
    @staticmethod
    def criar_professor(id_prof: int, nome: str, disponibilidade: dict, preferencias: list | None = None, semestre: str = "2026/1") -> Professor:
        if not nome or len(nome.strip()) < 3:
            raise ValueError("Nome do professor invalido (minimo 3 caracteres).")
        if not semestre.strip():
            raise ValueError("O semestre nao pode ser vazio.")
        return Professor(id_prof, nome, disponibilidade, preferencias or [], semestre)