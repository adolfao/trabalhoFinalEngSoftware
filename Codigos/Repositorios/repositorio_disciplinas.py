from typing import List
from Modelos.disciplina import Disciplina


class RepositorioDisciplinas:
    def __init__(self):
        self._disciplinas: List[Disciplina] = []

    def adicionar(self, disciplina: Disciplina):
        for i, d in enumerate(self._disciplinas):
            if d.codigo == disciplina.codigo:
                self._disciplinas[i] = disciplina
                return
        self._disciplinas.append(disciplina)

    def buscar_por_codigo(self, codigo: str):
        for d in self._disciplinas:
            if d.codigo == codigo:
                return d
        return None

    def remover(self, codigo: str) -> bool:
        """Remove a disciplina pelo código. Retorna True se removeu, False caso não exista."""
        tamanho_original = len(self._disciplinas)
        self._disciplinas = [d for d in self._disciplinas if d.codigo != codigo]
        return len(self._disciplinas) < tamanho_original

    def listar(self) -> List[Disciplina]:
        return list(self._disciplinas)