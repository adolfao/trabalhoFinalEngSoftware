"""
Interface de linha de comando para o sistema de alocacao de horarios.
O formulario de cadastro de professores segue o questionario proposto no TCC
(Camila Beatriz da Silva, UTFPR Apucarana, 2024), coletando indisponibilidades,
preferencias de turno e dias preferidos (matriz PV_pd do modelo matematico).
"""
from Fabricas.fabrica_professor import FabricaProfessor
from Fabricas.fabrica_disciplina import FabricaDisciplina
from Repositorios.repositorio_professores import RepositorioProfessores
from Repositorios.repositorio_disciplinas import RepositorioDisciplinas
from Repositorios.repositorio_vinculos import RepositorioVinculos
from Servicos.gerador_grade import GeradorGrade
from Servicos.validador_conflitos import ValidadorConflitos
from Servicos.organizador_horarios import OrganizadorHorarios
from Servicos.persistencia import Persistencia
from Modelos.horario import (
    HORARIOS_MANHA, HORARIOS_TARDE, TODOS_HORARIOS,
    DIAS_SEMANA, DESCRICAO_HORARIO, HORARIOS_BLOQUEADOS

)


def _ler_opcao(prompt: str, validas: list) -> str:
    while True:
        entrada = input(prompt).strip()
        if entrada in validas:
            return entrada
        print(f"  Opcao invalida. Valores aceitos: {validas}")


def _ler_indices(prompt: str, tamanho: int, obrigatorio: bool = True) -> list:
    """Lê indices separados por espaço. Retorna lista de inteiros 0-based."""
    while True:
        entrada = input(prompt).strip()
        if not obrigatorio and entrada == "":
            return []
        partes = entrada.split()
        indices = []
        valido = True
        for p in partes:
            if p.isdigit() and 1 <= int(p) <= tamanho:
                indices.append(int(p) - 1)
            else:
                valido = False
                break
        if valido and (not obrigatorio or len(indices) > 0):
            return indices
        print(f"  Digite numeros entre 1 e {tamanho}, separados por espaco.")


class InterfaceUsuario:
    def __init__(self):
        self.repo_profs = RepositorioProfessores()
        self.repo_discs = RepositorioDisciplinas()
        self.repo_vinculos = RepositorioVinculos()
        
        # 1. Carrega os dados do JSON
        Persistencia.carregar_dados(self.repo_profs, self.repo_discs)
        
        # 2. Calcula o próximo ID baseado no que foi carregado
        profs = self.repo_profs.listar()
        if profs:
            self._proximo_id = max([p.id_prof for p in profs]) + 1
        else:
            self._proximo_id = 1
            
        print(f"DEBUG: Repositório carregou {len(profs)} professores.")
        print(f"DEBUG: Próximo ID será {self._proximo_id}.")

        # 3. Inicializa variáveis de controle
        self._grade_atual = None
        self._grade_publicada = False

    def executar(self):
        print("\n" + "=" * 60)
        print("  SISTEMA DE ALOCACAO DE HORARIOS")
        print("  Engenharia de Computacao - UTFPR")
        print("=" * 60)
        opcoes = {
            "1": self._cadastrar_professor,
            "2": self._cadastrar_disciplina,
            "3": self._vincular_professor_disciplina,
            "4": self._gerar_grade,
            "5": self._ver_grade,
            "6": self._verificar_conflitos,
            "7": self._listar_dados,
            "8": self._remover_professor,
            "9": self._remover_disciplina,
            "10": self._visao_aluno,
            "11": self._publicar_grade,
        }
        while True:
            print("\n--- MENU ---")
            print("1. Cadastrar professor")
            print("2. Cadastrar disciplina")
            print("3. Vincular professor a disciplina")
            print("4. Gerar grade horaria")
            print("5. Ver grade atual")
            print("6. Verificar conflitos")
            print("7. Ver dados cadastrados")
            print("8. Remover professor")
            print("9. Remover disciplina")
            print("10. Visao do aluno (Grade por periodo)")
            print("11. Publicar grade horaria")
            print("0. Sair")
            opcao = input("\nEscolha: ").strip()
            if opcao == "0":
                print("\nEncerrando o sistema.")
                break
            acao = opcoes.get(opcao)
            if acao:
                try:
                    acao()
                except (KeyboardInterrupt, EOFError):
                    print("\nOperacao cancelada.")
            else:
                print("Opcao invalida.")

    # ------------------------------------------------------------------
    # Cadastro de professor (baseado no questionario do TCC, pag. 23)
    # ------------------------------------------------------------------
    def _cadastrar_professor(self):
        print(f"DEBUG: Antes de cadastrar, tenho {len(self.repo_profs.listar())} professores.")
        print("\n--- CADASTRO DE PROFESSOR ---")
        print("(Baseado no questionario de coleta de dados - TCC UTFPR Apucarana)")

        nome = input("Nome completo: ").strip()
        semestre = input("Semestre de validade (ex: 2026/1): ").strip()

        # Preferencia de turno (questao do formulario do TCC)
        print("\nPossui preferencia em qual periodo para ministrar aulas?")
        print("  1. Manha (M1-M6: 07:30 as 12:50)")
        print("  2. Tarde  (T1-T6: 13:00 as 18:20)")
        print("  3. Manha e tarde")
        turno = _ler_opcao("Escolha: ", ["1", "2", "3"])

        # Disposicao para M1 (questao especifica do TCC)
        aceita_m1 = False
        if turno in ("1", "3"):
            resp = _ler_opcao(
                "Estaria disposto a dar aulas as 07:30 (M1)? [s/n]: ", ["s", "n"]
            )
            aceita_m1 = resp == "s"

        # Monta os slots base conforme turno e disposicao para M1
        if turno == "1":
            slots_base = HORARIOS_MANHA if aceita_m1 else [h for h in HORARIOS_MANHA if h != "M1"]
        elif turno == "2":
            slots_base = list(HORARIOS_TARDE)
        else:
            manha = HORARIOS_MANHA if aceita_m1 else [h for h in HORARIOS_MANHA if h != "M1"]
            slots_base = manha + list(HORARIOS_TARDE)

        # Dias disponíveis
        print("\nQuais dias o professor PODE dar aulas?")
        for i, dia in enumerate(DIAS_SEMANA, 1):
            bloqueios = HORARIOS_BLOQUEADOS.get(dia, [])
            obs = f"  (obs: {', '.join(bloqueios)} bloqueados p/ reuniao)" if bloqueios else ""
            print(f"  {i}. {dia}{obs}")
        print("  ou digite 'todos' para selecionar todos os dias")
        entrada = input("Dias disponiveis (ex: 1 3 4): ").strip()

        if entrada.lower() == "todos":
            dias_disponiveis = list(DIAS_SEMANA)
        else:
            idx = _ler_indices("", len(DIAS_SEMANA))
            dias_disponiveis = [DIAS_SEMANA[i] for i in idx] if idx else list(DIAS_SEMANA)

        # Remove slots bloqueados do dia da reuniao
        disponibilidade = {}
        for dia in dias_disponiveis:
            bloqueados = HORARIOS_BLOQUEADOS.get(dia, [])
            slots_dia = [h for h in slots_base if h not in bloqueados]
            if slots_dia:
                disponibilidade[dia] = slots_dia

        if not disponibilidade:
            print("Nenhum slot disponivel apos aplicar restricoes. Cancelando.")
            return

        # Dias preferidos (PV_pd = 10 no modelo do TCC)
        print(f"\nDias preferidos para ministrar aulas (dentre os dias disponiveis):")
        dias_lista = list(disponibilidade.keys())
        for i, dia in enumerate(dias_lista, 1):
            print(f"  {i}. {dia}")
        print("  ou 'nenhum' para nao indicar preferencia")
        entrada_pref = input("Dias preferidos (ex: 1 3): ").strip()

        if entrada_pref.lower() == "nenhum":
            preferencias = []
        else:
            idx_pref = [int(x) - 1 for x in entrada_pref.split()
                        if x.isdigit() and 1 <= int(x) <= len(dias_lista)]
            preferencias = [dias_lista[i] for i in idx_pref]

        try:
            professor = FabricaProfessor.criar_professor(
                self._proximo_id, nome, disponibilidade, preferencias, semestre
            )
            self.repo_profs.adicionar(professor)
            print(f"DEBUG: Após cadastrar, tenho {len(self.repo_profs.listar())} professores.")
            self._proximo_id += 1

            Persistencia.salvar_dados(self.repo_profs, self.repo_discs)

            print(f"\nProfessor '{nome}' cadastrado (ID {professor.id_prof}).")
            print(f"  Dias disponiveis : {', '.join(disponibilidade.keys())}")
            if preferencias:
                print(f"  Dias preferidos  : {', '.join(preferencias)}")
            turno_desc = {"1": "Manha", "2": "Tarde", "3": "Manha e Tarde"}
            print(f"  Turno            : {turno_desc[turno]}"
                  + (" (incluindo 07:30)" if aceita_m1 else ""))
        except ValueError as e:
            print(f"Erro: {e}")

    # ------------------------------------------------------------------
    # Cadastro de disciplina
    # ------------------------------------------------------------------
    def _cadastrar_disciplina(self):
        print("\n--- CADASTRO DE DISCIPLINA ---")

        codigo = input("Codigo (ex: ES01): ").strip().upper()
        if not codigo:
            print("Codigo nao pode ser vazio.")
            return

        nome = input("Nome da disciplina: ").strip()
        if not nome:
            print("Nome nao pode ser vazio.")
            return
        
        turma = input("Turma (ex: A, B, Unica): ").strip()
        if not turma:
            print("Turma nao pode ser vazio.")
            return

        print("\nPeriodo/semestre da disciplina (1 a 10):")
        print("  Periodos impares -> aulas de manha (M1-M6)")
        print("  Periodos pares   -> aulas de tarde  (T1-T6)")
        while True:
            try:
                periodo = int(input("Periodo: ").strip())
                if 1 <= periodo <= 10:
                    break
                print("  Periodo deve ser entre 1 e 10.")
            except ValueError:
                print("  Digite um numero valido.")

        turno = "manha" if periodo % 2 != 0 else "tarde"
        print(f"  -> {periodo}o periodo: aulas no periodo da {turno}")

        print("\nCarga horaria semestral:")
        print("  1. 30h  (2 aulas/semana)")
        print("  2. 60h  (4 aulas/semana - sera dividida em 2 dias)")
        print("  3. 90h  (6 aulas/semana - sera dividida em 2 dias)")
        opcao_ch = _ler_opcao("Escolha: ", ["1", "2", "3"])
        carga_map = {"1": 30, "2": 60, "3": 90}
        carga_horaria = carga_map[opcao_ch]

        try:
            disciplina = FabricaDisciplina.criar_disciplina(codigo, nome, periodo, carga_horaria, turma)
            self.repo_discs.adicionar(disciplina)
            slots_sem = carga_horaria // 15
            Persistencia.salvar_dados(self.repo_profs, self.repo_discs)
            print(f"\nDisciplina '{nome}' cadastrada.")
            print(f"  Codigo  : {codigo} | Periodo: {periodo}o | {carga_horaria}h ({slots_sem} aulas/semana)")
        except ValueError as e:
            print(f"Erro: {e}")

    # ------------------------------------------------------------------
    # Vinculo professor -> disciplina
    # ------------------------------------------------------------------
    def _vincular_professor_disciplina(self):
        print("\n--- VINCULAR PROFESSOR A DISCIPLINA ---")

        professores = self.repo_profs.listar()
        disciplinas = self.repo_discs.listar()

        if not professores:
            print("Nenhum professor cadastrado. Use a opcao 1 primeiro.")
            return
        if not disciplinas:
            print("Nenhuma disciplina cadastrada. Use a opcao 2 primeiro.")
            return

        print("\nProfessores:")
        for i, p in enumerate(professores, 1):
            discs = self.repo_vinculos.listar_por_professor(p.id_prof)
            vinc_str = f"  -> {', '.join(d.nome for d in discs)}" if discs else ""
            print(f"  {i}. {p.nome}{vinc_str}")

        idx_p = _ler_indices("Escolha o professor: ", len(professores))
        if not idx_p:
            return
        professor = professores[idx_p[0]]

        print("\nDisciplinas:")
        for i, d in enumerate(disciplinas, 1):
            turno = "manha" if d.periodo % 2 != 0 else "tarde"
            slots = d.carga_horaria // 15
            print(f"  {i}. [{d.codigo}] {d.nome}  |  {d.periodo}o periodo ({turno})  |  {d.carga_horaria}h ({slots} aulas/sem)")

        idx_d = _ler_indices("Escolha a disciplina: ", len(disciplinas))
        if not idx_d:
            return
        disciplina = disciplinas[idx_d[0]]

        # Aviso se o professor nao tiver disponibilidade no turno necessario
        horarios_necessarios = HORARIOS_MANHA if disciplina.periodo % 2 != 0 else HORARIOS_TARDE
        slots_disponiveis = [
            h for dia_slots in professor.disponibilidade.values()
            for h in dia_slots if h in horarios_necessarios
        ]
        if not slots_disponiveis:
            turno_disc = "manha" if disciplina.periodo % 2 != 0 else "tarde"
            print(
                f"\n[Aviso] Prof. {professor.nome} nao tem disponibilidade no periodo da "
                f"{turno_disc}, que e o turno do {disciplina.periodo}o periodo. "
                f"O vinculo sera criado mas pode nao ser possivel alocar aulas."
            )

        self.repo_vinculos.adicionar(professor, disciplina)
        turno = "manha" if disciplina.periodo % 2 != 0 else "tarde"
        slots_sem = disciplina.carga_horaria // 15
        print(f"\nVinculo criado: Prof. {professor.nome} -> {disciplina.nome}")
        print(f"  {disciplina.periodo}o periodo ({turno}) | {slots_sem} aulas/semana")
        if professor.preferencias:
            print(f"  Dias preferidos do professor: {', '.join(professor.preferencias)}")

    # ------------------------------------------------------------------
    # Geracao de grade
    # ------------------------------------------------------------------
    def _gerar_grade(self):
        vinculos = self.repo_vinculos.listar()
        if not vinculos:
            print("\nNenhum vinculo cadastrado. Adicione vinculos (opcao 3) antes de gerar a grade.")
            return

        print(f"\n[Gerador] Gerando grade para {len(vinculos)} vinculo(s)...")
        gerador = GeradorGrade()
        self._grade_atual = gerador.gerar(vinculos)
        print(f"[Gerador] {len(self._grade_atual.alocacoes)} aulas alocadas na grade.")
        self._ver_grade()

    # ------------------------------------------------------------------
    # Visualizacao
    # ------------------------------------------------------------------
    def _ver_grade(self):
        if not self._grade_atual or not self._grade_atual.alocacoes:
            print("\nNenhuma grade gerada ainda. Use a opcao 4.")
            return
        print("\n[Grade] Horarios gerados:")
        OrganizadorHorarios().exibir(self._grade_atual)
        print(f"\nTotal: {len(self._grade_atual.alocacoes)} aulas alocadas.")

    # ------------------------------------------------------------------
    # Verificacao de conflitos
    # ------------------------------------------------------------------
    def _verificar_conflitos(self):
        if not self._grade_atual:
            print("\nNenhuma grade gerada ainda. Use a opcao 4.")
            return
        conflitos = ValidadorConflitos().executar_validacoes(self._grade_atual)
        if conflitos:
            print(f"\nCONFLITOS ENCONTRADOS ({len(conflitos)}):")
            for c in conflitos:
                print(f"  ! {c}")
        else:
            print("\nGrade sem conflitos!")

    # ------------------------------------------------------------------
    # Listagem geral
    # ------------------------------------------------------------------
    def _listar_dados(self):
        print("\n--- DADOS CADASTRADOS ---")

        profs = self.repo_profs.listar()
        print(f"\nProfessores ({len(profs)}):")
        for p in profs:
            dias = list(p.disponibilidade.keys())
            pref = f"  | Preferidos: {', '.join(p.preferencias)}" if p.preferencias else ""
            print(f"  [{p.id_prof}] {p.nome}  | Disponivel: {', '.join(dias)}{pref}")

        discs = self.repo_discs.listar()
        print(f"\nDisciplinas ({len(discs)}):")
        for d in discs:
            turno = "manha" if d.periodo % 2 != 0 else "tarde"
            slots = d.carga_horaria // 15
            print(f"  [{d.codigo}] {d.nome}  |  {d.periodo}o periodo ({turno})  |  {d.carga_horaria}h ({slots} aulas/sem)")

        vinculos = self.repo_vinculos.listar()
        print(f"\nVinculos ({len(vinculos)}):")
        for p, d in vinculos:
            print(f"  {p.nome}  ->  {d.nome} [{d.codigo}]  ({d.periodo}o periodo)")

        bloq = [f"{dia} {h}" for dia, hs in HORARIOS_BLOQUEADOS.items() for h in hs]
        print(f"\nHorarios bloqueados (reunioes): {', '.join(bloq)}")


    def _remover_professor(self):
            print("\n--- REMOVER PROFESSOR ---")
            profs = self.repo_profs.listar()
            if not profs:
                print("Nenhum professor cadastrado.")
                return

            for i, p in enumerate(profs, 1):
                print(f"  {i}. [{p.id_prof}] {p.nome}")
            
            idx = _ler_indices("Escolha o professor para remover: ", len(profs))
            if not idx:
                return
                
            prof = profs[idx[0]]
            self.repo_profs.remover(prof.id_prof)
            
            self.repo_vinculos._vinculos = [
                (p, d) for p, d in self.repo_vinculos.listar() if p.id_prof != prof.id_prof
            ]

            Persistencia.salvar_dados(self.repo_profs, self.repo_discs)

            print(f"\nProfessor '{prof.nome}' e seus vinculos foram removidos com sucesso.")

    def _remover_disciplina(self):
        print("\n--- REMOVER DISCIPLINA ---")
        discs = self.repo_discs.listar()
        if not discs:
            print("Nenhuma disciplina cadastrada.")
            return

        for i, d in enumerate(discs, 1):
            print(f"  {i}. [{d.codigo}] {d.nome}")
        
        idx = _ler_indices("Escolha a disciplina para remover: ", len(discs))
        if not idx:
            return
            
        disc = discs[idx[0]]
        self.repo_discs.remover(disc.codigo)
        
        # Limpa os vinculos associados a essa disciplina
        self.repo_vinculos._vinculos = [
            (p, d) for p, d in self.repo_vinculos.listar() if d.codigo != disc.codigo
        ]

        Persistencia.salvar_dados(self.repo_profs, self.repo_discs)

        print(f"\nDisciplina '{disc.nome}' e seus vinculos foram removidos com sucesso.")

    def _publicar_grade(self):
            """Atende ao critério de publicação da HU07."""
            if not self._grade_atual:
                print("\nNenhuma grade gerada para publicar.")
                return
            self._grade_publicada = True
            print("\n[Sucesso] Grade horaria PUBLICADA! Agora os alunos podem visualiza-la.")


    def _visao_aluno(self):
            """Atende a HU07: visualização do aluno após publicação."""
            print("\n--- VISAO DO ALUNO ---")
            if not self._grade_atual or not getattr(self, '_grade_publicada', False):
                print("A coordenacao ainda nao publicou nenhuma grade.")
                return
            
            try:
                periodo = int(input("Digite o seu periodo (1-10): ").strip())
            except ValueError:
                return
                
            org = OrganizadorHorarios()
            por_dia = org.por_dia(self._grade_atual)
            
            print(f"\n=== GRADE DO {periodo}o PERIODO ===")
            for dia, alocacoes in por_dia.items():
                aulas = [a for a in alocacoes if a["disciplina"].periodo == periodo]
                for a in aulas:
                    print(f" {dia} {a['horario']} - {a['disciplina'].nome} (Turma {a['disciplina'].turma})")
