import json
import os
from Modelos.disciplina import Disciplina
from Modelos.professor import Professor

class Persistencia:
    @staticmethod
    def salvar_dados(repo_profs, repo_discs):
        dados = {
            "professores": [
                {"id_prof": p.id_prof, "nome": p.nome, "disponibilidade": p.disponibilidade, 
                 "preferencias": p.preferencias, "semestre": p.semestre} for p in repo_profs.listar()
            ],
            "disciplinas": [
                {"codigo": d.codigo, "nome": d.nome, "periodo": d.periodo, 
                 "carga_horaria": d.carga_horaria, "turma": d.turma} for d in repo_discs.listar()
            ]
        }
        os.makedirs('data', exist_ok=True)
        with open('data/entities.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    @staticmethod
    def carregar_dados(repo_profs, repo_discs):
        if not os.path.exists('data/entities.json'):
            return

        with open('data/entities.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)

        for p_data in dados.get("professores", []):
            prof = Professor(p_data["id_prof"], p_data["nome"], p_data["disponibilidade"], 
                             p_data["preferencias"], p_data["semestre"])
            repo_profs.adicionar(prof)

        for d_data in dados.get("disciplinas", []):
            disc = Disciplina(d_data["codigo"], d_data["nome"], d_data["periodo"], 
                              d_data["carga_horaria"], d_data["turma"])
            repo_discs.adicionar(disc)