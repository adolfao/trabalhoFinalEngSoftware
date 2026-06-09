import os
import json
from typing import List

from Modelos.disciplina import Disciplina
from Modelos.professor import Professor


class RepositorioEntidades:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._data = {"professores": [], "disciplinas": []}
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                # Normaliza e remove duplicatas por chave (id_prof, codigo)
                profs = {}
                for p in raw.get("professores", []):
                    profs[p["id_prof"]] = p
                discs = {}
                for d in raw.get("disciplinas", []):
                    discs[d["codigo"]] = d
                self._data = {"professores": list(profs.values()), "disciplinas": list(discs.values())}
            except Exception:
                self._data = {"professores": [], "disciplinas": []}

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    # Professores
    def adicionar_professor(self, professor: Professor):
        # Atualiza se existir, caso contrário adiciona
        for i, p in enumerate(self._data["professores"]):
            if p.get("id_prof") == professor.id_prof:
                self._data["professores"][i] = {
                    "id_prof": professor.id_prof,
                    "nome": professor.nome,
                    "disponibilidade": professor.disponibilidade,
                }
                self._save()
                return
        self._data["professores"].append({
            "id_prof": professor.id_prof,
            "nome": professor.nome,
            "disponibilidade": professor.disponibilidade,
        })
        self._save()

    def listar_professores(self) -> List[Professor]:
        return [
            Professor(p["id_prof"], p["nome"], p.get("disponibilidade", {}))
            for p in self._data["professores"]
        ]

    # Disciplinas
    def adicionar_disciplina(self, disciplina: Disciplina):
        # Atualiza se existir por código, caso contrário adiciona
        for i, d in enumerate(self._data["disciplinas"]):
            if d.get("codigo") == disciplina.codigo:
                self._data["disciplinas"][i] = {
                    "codigo": disciplina.codigo,
                    "nome": disciplina.nome,
                    "periodo": disciplina.periodo,
                    "carga_horaria": disciplina.carga_horaria,
                }
                self._save()
                return
        self._data["disciplinas"].append({
            "codigo": disciplina.codigo,
            "nome": disciplina.nome,
            "periodo": disciplina.periodo,
            "carga_horaria": disciplina.carga_horaria,
        })
        self._save()

    def listar_disciplinas(self) -> List[Disciplina]:
        return [
            Disciplina(d["codigo"], d["nome"], d["periodo"], d["carga_horaria"])
            for d in self._data["disciplinas"]
        ]
