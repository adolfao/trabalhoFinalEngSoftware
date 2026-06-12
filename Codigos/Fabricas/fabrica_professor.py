from Modelos.professor import Professor

class FabricaProfessor:
    @staticmethod
    def criar_professor(id_prof: int, nome: str, disponibilidade: dict, preferencias: list = None) -> Professor:
        if not nome or len(nome.strip()) < 3:
            raise ValueError("Nome do professor inválido (mínimo 3 caracteres).")
        return Professor(id_prof, nome, disponibilidade, preferencias or [])
