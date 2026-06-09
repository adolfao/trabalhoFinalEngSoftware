import sys
import os

# Garante que o Python encontre os módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Fabricas.fabrica_professor import FabricaProfessor
from Fabricas.fabrica_disciplina import FabricaDisciplina
from Modelos.grade_horaria import GradeHoraria
from Servicos.validador_conflitos import ValidadorConflitos
from Servicos.gerenciador_entidades import RepositorioEntidades
import os

def executar_demonstracao():
    print("=== SISTEMA DE GESTÃO DE GRADE UNIVERSITÁRIA ===")
    print("Iniciando protótipo funcional para a Sprint 2...\n")

    try:
        # 1. Usando o padrão Factory Method e repositório simples para persistência em JSON
        print("[Factory+Repo] Criando e persistindo docentes e disciplinas...")
        storage = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "entities.json")
        repo = RepositorioEntidades(storage)

        prof1 = FabricaProfessor.criar_professor(1, "Lucio", {"Segunda": ["08:00"]})
        disc1 = FabricaDisciplina.criar_disciplina("ES01", "Engenharia de Software", 4, 60)
        disc2 = FabricaDisciplina.criar_disciplina("AL01", "Algoritmos", 4, 60)

        repo.adicionar_professor(prof1)
        repo.adicionar_disciplina(disc1)
        repo.adicionar_disciplina(disc2)

        print("[Repo] Professores cadastrados:")
        for p in repo.listar_professores():
            print(f" - {p.id_prof}: {p.nome}")

        print("[Repo] Disciplinas cadastradas:")
        for d in repo.listar_disciplinas():
            print(f" - {d.codigo}: {d.nome} ({d.periodo}º) - {d.carga_horaria}h")

        # 2. Montando uma grade horária e validando conflitos (HU06 / HU05)
        grade = GradeHoraria()
        grade.adicionar_aula(prof1, disc1, "Segunda", "08:00")
        grade.adicionar_aula(prof1, disc2, "Segunda", "08:00")
        print("[Grade] Aulas alocadas na memória.")

        print("\n[Strategy] Executando análise automática de conflitos...")
        validador = ValidadorConflitos()
        conflitos_encontrados = validador.executar_validacoes(grade)

        if conflitos_encontrados:
            print("\n CONFLITOS DETECTADOS NA GRADE:")
            for conflito in conflitos_encontrados:
                print(f"  - {conflito}")
        else:
            print("\n Grade validada com sucesso! Nenhum conflito encontrado.")

        # 3. Visualização textual simples da grade (HU06)
        print("\n[Visualizacao] Grade por dia e horário:")
        visualizar_grade_por_dia(grade)

    except Exception as e:
        print(f"\n💥 Erro inesperado no sistema: {e}")

def visualizar_grade_por_dia(grade: GradeHoraria):
    dias = {}
    for a in grade.alocacoes:
        dia = a["dia"]
        dias.setdefault(dia, []).append(a)

    for dia in sorted(dias.keys()):
        print(f"\n{dia}:")
        for a in sorted(dias[dia], key=lambda x: x["horario"]):
            prof = a["professor"].nome
            disc = a["disciplina"].nome
            horario = a["horario"]
            periodo = a["disciplina"].periodo
            print(f"  {horario} - {disc} (Período {periodo}) — Prof.: {prof}")

if __name__ == "__main__":
    executar_demonstracao()