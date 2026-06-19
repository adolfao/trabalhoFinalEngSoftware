from tabulate import tabulate

class GeradorRelatorio:
    @staticmethod
    def _diagnosticar_falha(prof, disc, grade_alocacoes, salas):
        """Investiga por que uma disciplina não pôde ser alocada nos horários livres do professor."""
        total_disp = sum(len(horarios) for horarios in prof.disponibilidade.values())
        aloc_prof = [a for a in grade_alocacoes if a['professor'].id_prof == prof.id_prof]
        
        if len(aloc_prof) >= total_disp:
            return "Agenda do professor 100% lotada."

        motivos = set()
        for dia, horarios in prof.disponibilidade.items():
            for h in horarios:
                # 1. O professor já está dando outra aula neste horário?
                aulas_deste_prof_agora = [a for a in aloc_prof if a['dia'] == dia and a['horario'] == h]
                if aulas_deste_prof_agora:
                    nome_outra = aulas_deste_prof_agora[0]['disciplina'].nome
                    
                    # CORREÇÃO AQUI: Se a aula for a própria disciplina que estamos analisando, 
                    # significa que foi um horário de sucesso! Ignoramos.
                    if nome_outra == disc.nome:
                        continue 
                        
                    motivos.add(f"Docente já alocado em '{nome_outra}'")
                    continue  

                # Pega todas as aulas do sistema acontecendo neste dia e horário
                aulas_neste_slot = [a for a in grade_alocacoes if a['dia'] == dia and a['horario'] == h]
                
                # 2. Os alunos já têm outra aula? (Choque de Período)
                conflitos_periodo = [a['disciplina'].nome for a in aulas_neste_slot if a['disciplina'].periodo == disc.periodo]
                if conflitos_periodo:
                    nomes_conflito = ", ".join(conflitos_periodo)
                    motivos.add(f"Turma do {disc.periodo}º per. ocupada com '{nomes_conflito}'")
                
                # 3. Faltou Sala Física?
                elif len(aulas_neste_slot) >= len(salas):
                    motivos.add("Lotação máxima de salas físicas excedida")

        if motivos:
            return " / ".join(list(motivos))
        return "Restrição do Otimizador (limite de aulas/dia ou quebra de blocos)"

    @staticmethod
    def salvar_txt(grade, vinculos, salas, caminho="relatorio_grade.txt"):
        """Salva a grade formatada e gera um diagnóstico profundo de não alocação."""
        
        # 1. Prepara os dados para a tabela principal
        dados = []
        for a in grade.alocacoes:
            dados.append([
                a['disciplina'].nome,
                a['professor'].nome,
                a['dia'],
                a['horario'],
                a['sala']
            ])

        headers = ["Disciplina", "Professor", "Dia", "Horário", "Sala"]
        tabela_formatada = tabulate(dados, headers=headers, tablefmt="grid")

        # 2. Verifica as disciplinas não alocadas e gera os diagnósticos
        alocadas_por_disc = {}
        for a in grade.alocacoes:
            codigo = a['disciplina'].codigo
            alocadas_por_disc[codigo] = alocadas_por_disc.get(codigo, 0) + 1
            
        avisos_faltantes = []
        for prof, disc in vinculos:
            slots_necessarios = disc.carga_horaria // 15
            slots_alocados = alocadas_por_disc.get(disc.codigo, 0)
            
            if slots_alocados < slots_necessarios:
                motivo = GeradorRelatorio._diagnosticar_falha(prof, disc, grade.alocacoes, salas)
                avisos_faltantes.append([
                    disc.nome, 
                    prof.nome, 
                    f"{slots_alocados}/{slots_necessarios} aulas",
                    motivo
                ])

        # 3. Escreve no arquivo de saída
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("=== RELATÓRIO DA GRADE HORÁRIA ===\n")
            f.write("Gerado em: 19/06/2026\n\n")
            f.write(tabela_formatada)
            f.write("\n\n")
            
            # Se houver erros, imprime a tabela de diagnósticos
            if avisos_faltantes:
                f.write("=== AUDITORIA DE NÃO ALOCAÇÃO ===\n")
                f.write("Abaixo estão as disciplinas com carga horária incompleta e o diagnóstico do sistema:\n\n")
                headers_avisos = ["Disciplina", "Docente", "Status", "Diagnóstico (Motivo)"]
                f.write(tabulate(avisos_faltantes, headers=headers_avisos, tablefmt="grid"))
                f.write("\n")
        
        print(f"Relatório formatado gerado em: {caminho}")