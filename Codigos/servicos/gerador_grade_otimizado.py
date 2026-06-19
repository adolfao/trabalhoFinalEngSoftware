"""
Gerador de grade horaria por OTIMIZACAO (modelo matematico MILP).

Reproduz em Python, com o solver CBC (via PuLP), o modelo de alocacao de
horarios proposto no TCC de Camila Beatriz da Silva (UTFPR Apucarana, 2024)
-- o mesmo documento usado como referencia neste projeto.

Diferenca para o GeradorGrade (heuristica gulosa):
  - A heuristica encontra UMA grade valida (first-fit, rapida).
  - Este gerador encontra a MELHOR grade segundo a funcao objetivo, satisfazendo
    todas as restricoes simultaneamente (otimizacao linear inteira).

Variavel de decisao (modelo do TCC: x_ptdh):
    x[i, d, h] = 1  se o vinculo i (professor + disciplina) tem aula no dia d,
                    horario h; 0 caso contrario.

Funcao objetivo:
    maximizar  PESO_ALOCACAO * (total de aulas alocadas)
             + PESO_PREFERENCIA * (aulas em dias preferidos do professor)
    Como PESO_ALOCACAO >> PESO_PREFERENCIA, preencher a carga horaria sempre
    vence; a preferencia de dia (matriz PV_pd do TCC) apenas desempata.

Restricoes implementadas (numeracao do TCC):
  (8)  carga horaria         -> cada vinculo recebe ATE os slots necessarios
                                (<=, garante que sempre exista solucao viavel)
  (9)  choque de turma       -> uma turma nao tem 2 aulas no mesmo slot
  (10) choque de docente     -> um professor nao tem 2 aulas no mesmo slot
  (11) periodo par/impar     -> impar de manha, par de tarde (dominio de h)
  (12) maximo de aulas/dia   -> <= MAXIMO_AULAS_DIA por professor por dia
  (13) disponibilidade       -> variavel so existe em (d,h) disponivel
  + horarios bloqueados      -> Terca M4-M5 (reuniao) fora do dominio
  + divisao da disciplina    -> 60h: 2/dia, 90h: 3/dia (regra do curso)
"""
from typing import List, Tuple

import pulp

from modelos.professor import Professor
from modelos.disciplina import Disciplina
from modelos.grade_horaria import GradeHoraria
from modelos.horario import (
    HORARIOS_MANHA, HORARIOS_TARDE, TODOS_HORARIOS, DIAS_SEMANA,
    MAXIMO_AULAS_DIA, HORARIOS_BLOQUEADOS,
)
from servicos.gerador_grade_base import GeradorGradeStrategy, atribuir_sala

# PESO_ALOCACAO >> PESO_PREFERENCIA: cada aula alocada vale muito mais que
# qualquer ganho de preferencia, entao o solver nunca deixa de alocar uma aula
# para satisfazer preferencia. A preferencia so escolhe entre grades de mesmo
# tamanho.
PESO_ALOCACAO = 100
PESO_PREFERENCIA = 1


def _max_slots_por_dia(slots_totais: int) -> int:
    """Disciplinas longas sao divididas em dias diferentes (TCC pag. 21).
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


class GeradorGradeOtimizado(GeradorGradeStrategy):
    def gerar(self, vinculos: List[Tuple[Professor, Disciplina]],
              salas: list) -> GradeHoraria:
        grade = GradeHoraria()
        if not vinculos or not salas:
            return grade

        problema = pulp.LpProblem("alocacao_horarios", pulp.LpMaximize)

        # --- Variaveis de decisao -------------------------------------------
        # Cria x[i,d,h] APENAS para combinacoes viaveis: respeita o turno do
        # periodo (restr. 11), a disponibilidade do professor (restr. 13) e os
        # horarios bloqueados. Restringir o dominio mantem o modelo pequeno.
        x = {}                  # (i, dia, horario) -> LpVariable binaria
        slots_necessarios = {}  # i -> int
        limite_por_dia = {}     # i -> int

        for i, (prof, disc) in enumerate(vinculos):
            slots_necessarios[i] = disc.carga_horaria // 15
            limite_por_dia[i] = _max_slots_por_dia(slots_necessarios[i])
            horarios_validos = (
                HORARIOS_MANHA if disc.periodo % 2 != 0 else HORARIOS_TARDE
            )
            for dia in DIAS_SEMANA:
                for h in horarios_validos:
                    if _slot_bloqueado(dia, h):
                        continue
                    if not prof.disponivel_em(dia, h):
                        continue
                    x[(i, dia, h)] = pulp.LpVariable(f"x_{i}_{dia}_{h}", cat="Binary")

        # --- Funcao objetivo ------------------------------------------------
        objetivo = []
        for (i, dia, _h), var in x.items():
            prof = vinculos[i][0]
            peso = PESO_ALOCACAO
            if dia in getattr(prof, "preferencias", []):
                peso += PESO_PREFERENCIA
            objetivo.append(peso * var)
        problema += pulp.lpSum(objetivo)

        # --- (8) Carga horaria: no maximo os slots necessarios --------------
        # --- Divisao da disciplina por dia (regra do curso) -----------------
        for i in range(len(vinculos)):
            vars_i = [v for k, v in x.items() if k[0] == i]
            if vars_i:
                problema += pulp.lpSum(vars_i) <= slots_necessarios[i], f"carga_{i}"
            for dia in DIAS_SEMANA:
                vars_id = [v for k, v in x.items() if k[0] == i and k[1] == dia]
                if vars_id:
                    problema += (
                        pulp.lpSum(vars_id) <= limite_por_dia[i],
                        f"divdia_{i}_{dia}",
                    )

        # --- Agrupamentos para as restricoes de choque ----------------------
        docente = {}    # (id_prof, dia, h)   -> [vars]  -> restr. (10)
        periodo = {}    # (periodo, dia, h)   -> [vars]  -> restr. (9)
        prof_dia = {}   # (id_prof, dia)      -> [vars]  -> restr. (12)
        slot = {}       # (dia, h)            -> [vars]  -> capacidade de salas
        for (i, dia, h), var in x.items():
            prof, disc = vinculos[i]
            docente.setdefault((prof.id_prof, dia, h), []).append(var)
            periodo.setdefault((disc.periodo, dia, h), []).append(var)
            prof_dia.setdefault((prof.id_prof, dia), []).append(var)
            slot.setdefault((dia, h), []).append(var)

        # --- (10) Choque de docente: 1 professor, 1 aula por slot -----------
        for (id_prof, dia, h), vs in docente.items():
            if len(vs) > 1:
                problema += pulp.lpSum(vs) <= 1, f"docente_{id_prof}_{dia}_{h}"

        # --- (9) Choque de periodo/turma: 1 aula por slot ------------------
        # Cada periodo tem uma unica turma por curso, logo duas disciplinas do
        # mesmo periodo nao podem ocorrer no mesmo dia e horario.
        for (per, dia, h), vs in periodo.items():
            if len(vs) > 1:
                problema += pulp.lpSum(vs) <= 1, f"periodo_{per}_{dia}_{h}"

        # --- (12) Maximo de aulas por professor por dia ---------------------
        for (id_prof, dia), vs in prof_dia.items():
            problema += pulp.lpSum(vs) <= MAXIMO_AULAS_DIA, f"maxdia_{id_prof}_{dia}"

        # --- Capacidade de salas: aulas simultaneas <= numero de salas ------
        for (dia, h), vs in slot.items():
            if len(vs) > len(salas):
                problema += pulp.lpSum(vs) <= len(salas), f"salas_{dia}_{h}"

        # --- Resolve --------------------------------------------------------
        problema.solve(pulp.PULP_CBC_CMD(msg=False))
        status = pulp.LpStatus[problema.status]
        if status not in ("Optimal", "Feasible"):
            print(f"[Otimizador] Solver retornou status '{status}'. Grade vazia.")
            return grade

        # --- Monta a grade a partir da solucao ------------------------------
        ordem_dia = {d: n for n, d in enumerate(DIAS_SEMANA)}
        ordem_h = {h: n for n, h in enumerate(TODOS_HORARIOS)}
        escolhidas = [
            (i, dia, h)
            for (i, dia, h), var in x.items()
            if var.value() is not None and var.value() > 0.5
        ]
        escolhidas.sort(key=lambda a: (ordem_dia[a[1]], ordem_h[a[2]]))

        alocados_por_vinculo = {}
        ocupado_sala = set()
        for i, dia, h in escolhidas:
            prof, disc = vinculos[i]
            sala = atribuir_sala(ocupado_sala, dia, h, salas)
            ocupado_sala.add((sala, dia, h))
            grade.adicionar_aula(prof, disc, dia, h, sala)
            alocados_por_vinculo[i] = alocados_por_vinculo.get(i, 0) + 1

        # --- Avisa sobre carga horaria nao atendida -------------------------
        for i, (prof, disc) in enumerate(vinculos):
            alocados = alocados_por_vinculo.get(i, 0)
            if alocados < slots_necessarios[i]:
                print(
                    f"[Aviso] So foi possivel alocar {alocados}/{slots_necessarios[i]} "
                    f"aulas de '{disc.nome}' com Prof. {prof.nome} "
                    f"(disponibilidade insuficiente no turno)."
                )

        return grade
