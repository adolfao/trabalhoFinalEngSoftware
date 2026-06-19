from abc import ABC, abstractmethod
from typing import List
from modelos.grade_horaria import GradeHoraria

class EstrategiaValidacao(ABC):
    @abstractmethod
    def validar(self, grade: GradeHoraria) -> List[str]:
        pass

class ValidaChoqueDocente(EstrategiaValidacao):
    def validar(self, grade: GradeHoraria) -> List[str]:
        conflitos = []
        vistos = set()
        for alocacao in grade.alocacoes:
            # Chave única: professor, dia e horário
            chave = (alocacao["professor"].id_prof, alocacao["dia"], alocacao["horario"])
            if chave in vistos:
                conflitos.append(f"Conflito: O professor {alocacao['professor'].nome} está alocado em duas turmas no mesmo horário ({alocacao['dia']} às {alocacao['horario']}).")
            vistos.add(chave)
        return conflitos

class ValidaChoquePeriodo(EstrategiaValidacao):
    def validar(self, grade: GradeHoraria) -> List[str]:
        conflitos = []
        vistos = set()
        for alocacao in grade.alocacoes:
            # Cada periodo tem uma unica turma por curso: a chave e
            # periodo + dia + horario.
            chave = (alocacao["disciplina"].periodo, alocacao["dia"], alocacao["horario"])
            if chave in vistos:
                conflitos.append(f"Conflito: O {alocacao['disciplina'].periodo}º Período tem duas disciplinas no mesmo horário ({alocacao['dia']} às {alocacao['horario']}).")
            vistos.add(chave)
        return conflitos

class ValidaChoqueSala(EstrategiaValidacao):
    def validar(self, grade: GradeHoraria) -> List[str]:
        conflitos = []
        vistos = set()
        for alocacao in grade.alocacoes:
            sala = alocacao.get("sala")
            if sala is None:
                continue
            # Chave única: sala (local físico), dia e horário.
            chave = (sala, alocacao["dia"], alocacao["horario"])
            if chave in vistos:
                conflitos.append(f"Conflito: {sala} tem duas aulas no mesmo horário ({alocacao['dia']} às {alocacao['horario']}).")
            vistos.add(chave)
        return conflitos

class ValidadorConflitos:
    def __init__(self):
        self._estrategias: List[EstrategiaValidacao] = [
            ValidaChoqueDocente(),
            ValidaChoquePeriodo(),
            ValidaChoqueSala()
        ]

    def executar_validacoes(self, grade: GradeHoraria) -> List[str]:
        todos_conflitos = []
        for estrategia in self._estrategias:
            todos_conflitos.extend(estrategia.validar(grade))
        return todos_conflitos