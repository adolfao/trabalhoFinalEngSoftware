"""Leitura da entrada estruturada do sistema.

O sistema recebe como entrada um arquivo JSON (e nao uma interface interativa),
contendo professores, disciplinas e os vinculos entre eles. Cada entidade e
criada pelas Fabricas (Factory Method), que validam os dados antes de aceitar.

Formato esperado do arquivo:
{
  "professores": [
    {"id_prof": 1, "nome": "...",
     "disponibilidade": {"Terca": ["T1", "T2"]},
     "preferencias": ["Sexta"]}
  ],
  "disciplinas": [
    {"codigo": "ENCO6A", "nome": "...", "periodo": 6,
     "carga_horaria": 60, "turma": "A"}
  ],
  "vinculos": [
    {"id_prof": 1, "codigo": "ENCO6A"}
  ],
  "salas": ["Sala 1", "Sala 2"]
}

A chave "salas" e opcional: se ausente, assume-se uma sala por periodo distinto.
"""
import json
from typing import List, Tuple

from fabricas.fabrica_professor import FabricaProfessor
from fabricas.fabrica_disciplina import FabricaDisciplina
from modelos.professor import Professor
from modelos.disciplina import Disciplina


class LeitorEntrada:
    @staticmethod
    def ler(caminho: str) -> Tuple[List[Professor], List[Disciplina],
                                   List[Tuple[Professor, Disciplina]], list]:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        professores = {}
        for p in dados.get("professores", []):
            prof = FabricaProfessor.criar_professor(
                p["id_prof"], p["nome"], p.get("disponibilidade", {}),
                p.get("preferencias", []), p.get("semestre", "2026/1"),
            )
            professores[prof.id_prof] = prof

        disciplinas = {}
        for d in dados.get("disciplinas", []):
            disc = FabricaDisciplina.criar_disciplina(
                d["codigo"], d["nome"], d["periodo"], d["carga_horaria"],
                d.get("turma", "Unica"),
            )
            disciplinas[disc.codigo] = disc

        vinculos = []
        for v in dados.get("vinculos", []):
            prof = professores.get(v["id_prof"])
            disc = disciplinas.get(v["codigo"])
            if prof is None:
                raise ValueError(
                    f"Vinculo invalido: professor de id {v['id_prof']} nao cadastrado."
                )
            if disc is None:
                raise ValueError(
                    f"Vinculo invalido: disciplina '{v['codigo']}' nao cadastrada."
                )
            vinculos.append((prof, disc))

        # Salas (locais fisicos). Sem "salas" no arquivo, assume uma sala por
        # periodo distinto, garantindo capacidade suficiente para a grade.
        salas = list(dados.get("salas", []))
        if not salas:
            periodos = {d.periodo for d in disciplinas.values()}
            salas = [f"Sala {i + 1}" for i in range(max(1, len(periodos)))]

        return (list(professores.values()), list(disciplinas.values()),
                vinculos, salas)
