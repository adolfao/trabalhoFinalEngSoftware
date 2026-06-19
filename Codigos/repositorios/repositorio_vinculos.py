from typing import List, Tuple
from modelos.professor import Professor
from modelos.disciplina import Disciplina


class RepositorioVinculos:
    def __init__(self):
        self._vinculos: List[Tuple[Professor, Disciplina]] = []

    def adicionar(self, professor: Professor, disciplina: Disciplina):
        for p, d in self._vinculos:
            if p.id_prof == professor.id_prof and d.codigo == disciplina.codigo:
                return
        self._vinculos.append((professor, disciplina))

    def remover(self, id_prof: int, codigo: str):
        self._vinculos = [
            (p, d) for p, d in self._vinculos
            if not (p.id_prof == id_prof and d.codigo == codigo)
        ]

    def listar(self) -> List[Tuple[Professor, Disciplina]]:
        return list(self._vinculos)

    def listar_por_professor(self, id_prof: int) -> List[Disciplina]:
        return [d for p, d in self._vinculos if p.id_prof == id_prof]
