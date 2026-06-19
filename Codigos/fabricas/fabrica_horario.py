from modelos.horario import TODOS_HORARIOS, DIAS_SEMANA


class FabricaHorario:
    @staticmethod
    def criar_disponibilidade(dias: list, horarios: list) -> dict:
        """Cria dicionário de disponibilidade {dia: [slots]} validando as entradas."""
        for dia in dias:
            if dia not in DIAS_SEMANA:
                raise ValueError(f"Dia inválido: '{dia}'. Valores aceitos: {DIAS_SEMANA}")
        for horario in horarios:
            if horario not in TODOS_HORARIOS:
                raise ValueError(f"Horário inválido: '{horario}'. Valores aceitos: {TODOS_HORARIOS}")
        return {dia: list(horarios) for dia in dias}
