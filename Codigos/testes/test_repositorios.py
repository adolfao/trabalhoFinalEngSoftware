import pytest
from modelos.professor import Professor
from repositorios.repositorio_professores import RepositorioProfessores

@pytest.fixture
def repo():
    return RepositorioProfessores()

@pytest.fixture
def prof_valido():
    return Professor(1, "Luiz", {}, [], "2026/1")

# --- TESTES DO REPOSITÓRIO ---

def test_adicionar_professor_sucesso(repo, prof_valido):
    """Caso de Sucesso: Adicionar um professor novo à lista."""
    repo.adicionar(prof_valido)
    assert len(repo.listar()) == 1
    assert repo.listar()[0].nome == "Luiz"

def test_adicionar_professor_falha_id_duplicado(repo, prof_valido):
    """Caso de Falha: Adicionar professor com ID duplicado deve sobrescrever (segundo a sua regra atual)."""
    repo.adicionar(prof_valido)
    prof_duplicado = Professor(1, "Luiz Alterado", {}, [], "2026/1")
    repo.adicionar(prof_duplicado)
    
    lista = repo.listar()
    assert len(lista) == 1
    assert lista[0].nome == "Luiz Alterado"

def test_remover_professor_borda_inexistente(repo):
    """Caso de Borda: Remover ID inexistente não deve quebrar o sistema."""
    resultado = repo.remover(999) # ID que não existe
    assert resultado is False
    assert len(repo.listar()) == 0