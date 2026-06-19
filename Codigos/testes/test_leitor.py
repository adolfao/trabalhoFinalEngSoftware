import pytest
import json
import os
from servicos.leitor_entrada import LeitorEntrada

# Fixture para criar um arquivo temporário antes de cada teste
@pytest.fixture
def arquivo_teste(tmp_path):
    d = tmp_path / "teste.json"
    return d

def test_leitura_sucesso(arquivo_teste):
    """Caso de Sucesso: O leitor processa dados válidos corretamente."""
    dados = {
        "professores": [{"id_prof": 1, "nome": "Luiz", "disponibilidade": {"Segunda": ["T1"]}}],
        "disciplinas": [{"codigo": "ES01", "nome": "Eng", "periodo": 4, "carga_horaria": 60}],
        "vinculos": [{"id_prof": 1, "codigo": "ES01"}]
    }
    arquivo_teste.write_text(json.dumps(dados), encoding="utf-8")
    
    profs, discs, vincs, salas = LeitorEntrada.ler(str(arquivo_teste))
    
    assert len(profs) == 1
    assert len(discs) == 1
    assert len(vincs) == 1
    assert salas == ["Sala 1"]

def test_falha_vinculo_invalido(arquivo_teste):
    """Caso de Falha: O sistema deve levantar ValueError para vínculos inexistentes."""
    dados = {
        "professores": [{"id_prof": 1, "nome": "Luiz"}],
        "disciplinas": [{"codigo": "ES01", "nome": "Eng", "periodo": 4, "carga_horaria": 60}],
        "vinculos": [{"id_prof": 99, "codigo": "ES01"}] # ID 99 não existe
    }
    arquivo_teste.write_text(json.dumps(dados), encoding="utf-8")
    
    with pytest.raises(ValueError, match="Vinculo invalido"):
        LeitorEntrada.ler(str(arquivo_teste))

def test_borda_salas_ausentes(arquivo_teste):
    """Caso de Borda: Arquivo sem chave 'salas' deve gerar sala padrão."""
    dados = {
        "professores": [],
        "disciplinas": [{"codigo": "AL01", "nome": "Alg", "periodo": 2, "carga_horaria": 60}]
    }
    arquivo_teste.write_text(json.dumps(dados), encoding="utf-8")
    
    _, _, _, salas = LeitorEntrada.ler(str(arquivo_teste))
    
    # Deve criar "Sala 1" automaticamente para o período 2
    assert salas == ["Sala 1"]