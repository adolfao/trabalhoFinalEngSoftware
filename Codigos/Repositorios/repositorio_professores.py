from typing import List
from Modelos.professor import Professor


class RepositorioProfessores:
    def __init__(self):
        self._professores: List[Professor] = []

    def adicionar(self, professor: Professor):
        for i, p in enumerate(self._professores):
            if p.id_prof == professor.id_prof:
                self._professores[i] = professor
                return
        self._professores.append(professor)

    def buscar_por_id(self, id_prof: int):
        for p in self._professores:
            if p.id_prof == id_prof:
                return p
        return None

    def remover(self, id_prof: int) -> bool:
        """Remove o professor pelo ID. Retorna True se removeu, False caso não exista."""
        tamanho_original = len(self._professores)
        self._professores = [p for p in self._professores if p.id_prof != id_prof]
        return len(self._professores) < tamanho_original

    def listar(self) -> List[Professor]:
        return list(self._professores)