"""Ponto de entrada do sistema de geracao de grade horaria.

Uso:
    python main.py [arquivo_entrada.json] [metodo]

  - arquivo_entrada.json : caminho do arquivo de entrada (padrao: entrada.json)
  - metodo               : "otimizacao" (padrao) ou "heuristica"

O sistema le os dados estruturados do arquivo, gera a grade horaria com a
estrategia escolhida, valida conflitos e imprime o relatorio no terminal.
"""
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from servicos.leitor_entrada import LeitorEntrada
from servicos.gerador_grade import GeradorGrade
from servicos.validador_conflitos import ValidadorConflitos
from servicos.organizador_horarios import OrganizadorHorarios


def selecionar_gerador(metodo: str):
    """Escolhe a estrategia de geracao (padrao Strategy)."""
    if metodo == "heuristica":
        return GeradorGrade()
    try:
        from servicos.gerador_grade_otimizado import GeradorGradeOtimizado
        return GeradorGradeOtimizado()
    except ImportError:
        print("[Aviso] PuLP nao instalado; usando a heuristica.")
        print("        Para a otimizacao: pip install -r requirements.txt")
        return GeradorGrade()


def main(argv) -> int:
    base = os.path.dirname(os.path.abspath(__file__))
    caminho = argv[1] if len(argv) > 1 else os.path.join(base, "entrada.json")
    metodo = argv[2] if len(argv) > 2 else "otimizacao"

    if not os.path.exists(caminho):
        print(f"Arquivo de entrada nao encontrado: {caminho}")
        return 1

    try:
        professores, disciplinas, vinculos, salas = LeitorEntrada.ler(caminho)
    except (ValueError, KeyError, json.JSONDecodeError) as erro:
        print(f"Erro na leitura da entrada: {erro}")
        return 1

    print("=" * 60)
    print("  SISTEMA DE GERACAO DE GRADE HORARIA")
    print("  Engenharia de Computacao - UTFPR")
    print("=" * 60)
    print(f"Entrada   : {caminho}")
    print(f"Metodo    : {metodo}")
    print(f"Dados     : {len(professores)} professores, "
          f"{len(disciplinas)} disciplinas, {len(vinculos)} vinculos, "
          f"{len(salas)} salas")

    gerador = selecionar_gerador(metodo)
    grade = gerador.gerar(vinculos, salas)

    print(f"\n--- GRADE GERADA ({len(grade.alocacoes)} aulas) ---")
    OrganizadorHorarios().exibir(grade)

    print("\n--- VALIDACAO DE CONFLITOS ---")
    conflitos = ValidadorConflitos().executar_validacoes(grade)
    if conflitos:
        print(f"{len(conflitos)} conflito(s) encontrado(s):")
        for c in conflitos:
            print(f"  ! {c}")
    else:
        print("Nenhum conflito encontrado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
