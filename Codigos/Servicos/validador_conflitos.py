from abc import ABC, abstractmethod
from typing import List
from Modelos.grade_horaria import GradeHoraria
from Modelos.horario import HORARIOS_BLOQUEADOS, DESCRICAO_HORARIO


class EstrategiaValidacao(ABC):
    @abstractmethod
    def validar(self, grade: GradeHoraria) -> List[str]:
        pass


class ValidaChoqueDocente(EstrategiaValidacao):
    """Mesmo professor nao pode estar em dois lugares ao mesmo tempo (restricao 10 do TCC)."""
    def validar(self, grade: GradeHoraria) -> List[str]:
        conflitos = []
        vistos = set()
        for alocacao in grade.alocacoes:
            chave = (alocacao["professor"].id_prof, alocacao["dia"], alocacao["horario"])
            if chave in vistos:
                conflitos.append(
                    f"Conflito de docente: Prof. {alocacao['professor'].nome} esta alocado "
                    f"em duas turmas em {alocacao['dia']} {alocacao['horario']}."
                )
            vistos.add(chave)
        return conflitos


class ValidaChoquePeriodo(EstrategiaValidacao):
    """Mesmo periodo nao pode ter duas disciplinas no mesmo slot (restricao 9 do TCC)."""
    def validar(self, grade: GradeHoraria) -> List[str]:
        conflitos = []
        vistos = set()
        for alocacao in grade.alocacoes:
            chave = (alocacao["disciplina"].periodo, alocacao["dia"], alocacao["horario"])
            if chave in vistos:
                conflitos.append(
                    f"Conflito de periodo: {alocacao['disciplina'].periodo}o periodo tem "
                    f"duas disciplinas em {alocacao['dia']} {alocacao['horario']}."
                )
            vistos.add(chave)
        return conflitos


class ValidaHorarioReuniao(EstrategiaValidacao):
    """Terca-feira M4 e M5 reservados para reuniao dos professores (TCC pag. 21)."""
    def validar(self, grade: GradeHoraria) -> List[str]:
        conflitos = []
        for alocacao in grade.alocacoes:
            dia = alocacao["dia"]
            horario = alocacao["horario"]
            if horario in HORARIOS_BLOQUEADOS.get(dia, []):
                descricao = DESCRICAO_HORARIO.get(horario, horario)
                conflitos.append(
                    f"Conflito de reuniao: '{alocacao['disciplina'].nome}' alocada na "
                    f"Terca {horario} ({descricao}), horario reservado para reuniao dos professores."
                )
        return conflitos


class ValidaDisponibilidadeProfessor(EstrategiaValidacao):
    """Professor nao pode dar aula em slot fora de sua disponibilidade (restricao 13 do TCC)."""
    def validar(self, grade: GradeHoraria) -> List[str]:
        conflitos = []
        for alocacao in grade.alocacoes:
            prof = alocacao["professor"]
            dia = alocacao["dia"]
            horario = alocacao["horario"]
            if not prof.disponivel_em(dia, horario):
                conflitos.append(
                    f"Conflito de disponibilidade: Prof. {prof.nome} nao esta disponivel "
                    f"em {dia} {horario}, mas foi alocado."
                )
        return conflitos


class ValidadorConflitos:
    def __init__(self):
        self._estrategias: List[EstrategiaValidacao] = [
            ValidaChoqueDocente(),
            ValidaChoquePeriodo(),
            ValidaHorarioReuniao(),
            ValidaDisponibilidadeProfessor(),
        ]

    def executar_validacoes(self, grade: GradeHoraria) -> List[str]:
        todos_conflitos = []
        for estrategia in self._estrategias:
            todos_conflitos.extend(estrategia.validar(grade))
        return todos_conflitos
