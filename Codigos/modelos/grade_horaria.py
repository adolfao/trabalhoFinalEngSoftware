class GradeHoraria:
    def __init__(self):
        # Lista de dicionarios: {professor, disciplina, dia, horario, sala}
        self.alocacoes = []

    def adicionar_aula(self, professor, disciplina, dia, horario, sala=None):
        self.alocacoes.append({
            "professor": professor,
            "disciplina": disciplina,
            "dia": dia,
            "horario": horario,
            "sala": sala,
        })
