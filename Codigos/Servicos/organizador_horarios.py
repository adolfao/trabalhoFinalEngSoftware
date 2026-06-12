from Modelos.grade_horaria import GradeHoraria
from Modelos.horario import TODOS_HORARIOS, DESCRICAO_HORARIO, DIAS_SEMANA


class OrganizadorHorarios:
    def por_dia(self, grade: GradeHoraria) -> dict:
        """Agrupa as alocações por dia da semana, ordenadas por horário."""
        resultado = {dia: [] for dia in DIAS_SEMANA}
        for alocacao in grade.alocacoes:
            dia = alocacao["dia"]
            if dia in resultado:
                resultado[dia].append(alocacao)
        for dia in resultado:
            resultado[dia].sort(
                key=lambda a: TODOS_HORARIOS.index(a["horario"])
                if a["horario"] in TODOS_HORARIOS else 99
            )
        return resultado

    def por_periodo(self, grade: GradeHoraria) -> dict:
        """Agrupa as alocações por período/semestre."""
        resultado = {}
        for alocacao in grade.alocacoes:
            periodo = alocacao["disciplina"].periodo
            resultado.setdefault(periodo, []).append(alocacao)
        return resultado

    def exibir(self, grade: GradeHoraria):
        """Imprime a grade formatada por dia e horário."""
        por_dia = self.por_dia(grade)
        for dia, alocacoes in por_dia.items():
            if not alocacoes:
                continue
            print(f"\n{dia}:")
            for a in alocacoes:
                horario = a["horario"]
                inicio = DESCRICAO_HORARIO.get(horario, horario)
                print(
                    f"  {horario} ({inicio}) - {a['disciplina'].nome} "
                    f"[{a['disciplina'].periodo}o periodo] "
                    f"- Prof. {a['professor'].nome}"
                )
