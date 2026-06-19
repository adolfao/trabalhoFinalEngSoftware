"""Interface (Strategy) para os geradores de grade horaria.

Permite que o sistema troque o algoritmo de geracao da grade sem alterar quem
o utiliza (padrao Strategy). Hoje existem duas estrategias concretas:
  - GeradorGrade            -> heuristica gulosa (rapida)
  - GeradorGradeOtimizado   -> otimizacao linear inteira / MILP (melhor grade)

Cada aula da grade e alocada em uma sala (local fisico). Duas aulas nao podem
ocupar a mesma sala no mesmo dia e horario.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple

from modelos.professor import Professor
from modelos.disciplina import Disciplina
from modelos.grade_horaria import GradeHoraria


def atribuir_sala(ocupadas: set, dia: str, horario: str, salas: list):
    """Retorna a primeira sala livre em (dia, horario) ou None se todas ocupadas.

    `ocupadas` e um conjunto de chaves (sala, dia, horario) ja utilizadas.
    """
    for sala in salas:
        if (sala, dia, horario) not in ocupadas:
            return sala
    return None


class GeradorGradeStrategy(ABC):
    @abstractmethod
    def gerar(self, vinculos: List[Tuple[Professor, Disciplina]],
              salas: list) -> GradeHoraria:
        """Gera uma grade a partir dos vinculos (professor, disciplina),
        alocando cada aula em uma das `salas` disponiveis."""
        raise NotImplementedError
