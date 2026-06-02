class GradeHoraria:
    def __init__(self):
        # Lista de dicionários contendo {professor, disciplina, dia, horario}
        self.alocacoes = []

    def adicionar_aula(self, professor, disciplina, dia, horario):
        self.alocacoes.append({
            "professor": professor,
            "disciplina": disciplina,
            "dia": dia,
            "horario": horario
        })