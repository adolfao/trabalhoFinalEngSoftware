import sys
import os

# Garante que o Python encontre os módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fabricas.fabrica_professor import FabricaProfessor
from fabricas.fabrica_disciplina import FabricaDisciplina
from modelos.grade_horaria import GradeHoraria
from servicos.validador_conflitos import ValidadorConflitos

def executar_demonstracao():
    print("=== SISTEMA DE GESTÃO DE GRADE UNIVERSITÁRIA ===")
    print("Iniciando protótipo funcional para a Sprint 2...\n")

    try:
        # 1. Usando o padrão Factory Method para instanciar com segurança
        print("[Factory] Criando docentes e disciplinas...")
        prof1 = FabricaProfessor.criar_professor(1, "Dr. Adolfo", {"segunda": ["08:00"]})
        disc1 = FabricaDisciplina.criar_disciplina("ES01", "Engenharia de Software", 4, 60)
        disc2 = FabricaDisciplina.criar_disciplina("AL01", "Algoritmos", 4, 60)
        
        # 2. Montando uma grade horária
        grade = GradeHoraria()
        
        # Simulando um conflito clássico: Mesmo período (4º) com duas aulas na Segunda às 08:00
        grade.adicionar_aula(prof1, disc1, "Segunda", "08:00")
        grade.adicionar_aula(prof1, disc2, "Segunda", "08:00")
        print("[Grade] Aulas alocadas na memória.")

        # 3. Executando a validação com o padrão Strategy
        print("\n[Strategy] Executando análise automática de conflitos...")
        validador = ValidadorConflitos()
        conflitos_encontrados = validador.executar_validacoes(grade)

        if conflitos_encontrados:
            print("\n CONFLITOS DETECTADOS NA GRADE:")
            for conflito in conflitos_encontrados:
                print(f"  - {conflito}")
        else:
            print("\n Grade validada com sucesso! Nenhum conflito encontrado.")

    except Exception as e:
        print(f"\n💥 Erro inesperado no sistema: {e}")

if __name__ == "__main__":
    executar_demonstracao()