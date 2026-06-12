from typing import List, Tuple
from Modelos.professor import Professor
from Modelos.disciplina import Disciplina
from Modelos.grade_horaria import GradeHoraria
from Modelos.horario import (
    HORARIOS_MANHA, HORARIOS_TARDE, DIAS_SEMANA,
    MAXIMO_AULAS_DIA, HORARIOS_BLOQUEADOS
)


def _max_slots_por_dia(slots_totais: int) -> int:
    """
    Disciplinas com mais de 3 horas semanais devem ser divididas em dias diferentes.
    (TCC pag. 21: '4 horas-aula sao divididas em 2 dias com 2 horas cada')
      30h -> 2 slots -> podem ficar no mesmo dia
      60h -> 4 slots -> max 2 por dia (2+2)
      90h -> 6 slots -> max 3 por dia (3+3)
    """
    if slots_totais <= 2:
        return slots_totais
    if slots_totais == 4:
        return 2
    return 3  # 6 slots


def _slot_bloqueado(dia: str, horario: str) -> bool:
    return horario in HORARIOS_BLOQUEADOS.get(dia, [])


class GeradorGrade:
    def gerar(self, vinculos: List[Tuple[Professor, Disciplina]]) -> GradeHoraria:
        """
        Gera grade horaria respeitando as restricoes do curso de Engenharia de Computacao
        da UTFPR Campus Apucarana (TCC - Camila Beatriz da Silva, 2024):

        - Periodos impares -> manha (M1-M6); pares -> tarde (T1-T6)  [restricao 11]
        - Sem choque de docente: prof. nao pode estar em dois lugares ao mesmo tempo [restr. 10]
        - Sem choque de periodo: um periodo nao pode ter duas disciplinas no mesmo slot [restr. 9]
        - Disponibilidade do professor (Disp_pdh)  [restricao 13]
        - Maximo de 7 aulas por professor por dia  [restricao 12]
        - Terca M4-M5 bloqueados (reuniao dos professores)
        - Disciplinas com 4+ slots semanais divididas em dias diferentes  [regra do curso]
        - Dias preferidos do professor alocados primeiro (PV_pd = 10)
        """
        grade = GradeHoraria()
        ocupado_prof = set()       # (id_prof, dia, horario)
        ocupado_periodo = set()    # (periodo, dia, horario)
        aulas_por_prof_dia = {}    # (id_prof, dia) -> int
        slots_disc_dia = {}        # (codigo_disc, dia) -> int  -- para forcar divisao

        for professor, disciplina in vinculos:
            # 30h->2 slots/sem, 60h->4, 90h->6  (semestre de 15 semanas)
            slots_necessarios = disciplina.carga_horaria // 15
            limite_por_dia = _max_slots_por_dia(slots_necessarios)
            horarios_validos = (
                HORARIOS_MANHA if disciplina.periodo % 2 != 0 else HORARIOS_TARDE
            )
            # Dias preferidos primeiro (PV_pd = 10 > 5 no modelo do TCC)
            dias_ordenados = sorted(
                DIAS_SEMANA,
                key=lambda d: (0 if d in professor.preferencias else 1)
            )
            slots_alocados = 0

            for dia in dias_ordenados:
                if slots_alocados >= slots_necessarios:
                    break
                for horario in horarios_validos:
                    if slots_alocados >= slots_necessarios:
                        break

                    if _slot_bloqueado(dia, horario):
                        continue
                    if not professor.disponivel_em(dia, horario):
                        continue
                    if (professor.id_prof, dia, horario) in ocupado_prof:
                        continue
                    if (disciplina.periodo, dia, horario) in ocupado_periodo:
                        continue
                    if aulas_por_prof_dia.get((professor.id_prof, dia), 0) >= MAXIMO_AULAS_DIA:
                        continue
                    if slots_disc_dia.get((disciplina.codigo, dia), 0) >= limite_por_dia:
                        continue

                    grade.adicionar_aula(professor, disciplina, dia, horario)
                    ocupado_prof.add((professor.id_prof, dia, horario))
                    ocupado_periodo.add((disciplina.periodo, dia, horario))
                    aulas_por_prof_dia[(professor.id_prof, dia)] = (
                        aulas_por_prof_dia.get((professor.id_prof, dia), 0) + 1
                    )
                    slots_disc_dia[(disciplina.codigo, dia)] = (
                        slots_disc_dia.get((disciplina.codigo, dia), 0) + 1
                    )
                    slots_alocados += 1

            if slots_alocados < slots_necessarios:
                print(
                    f"[Aviso] Nao foi possivel alocar todos os {slots_necessarios} slots "
                    f"para '{disciplina.nome}' com Prof. {professor.nome} "
                    f"(alocados: {slots_alocados})."
                )

        return grade
