import pytest
from fabricas.fabrica_disciplina import FabricaDisciplina

def test_fabrica_disciplina_carga_invalida():
    """Caso de Falha: A fábrica deve rejeitar carga horária fora dos padrões (ex: 50h)."""
    # O ".*" no final diz ao pytest: "verifique se começa com isso, o resto não importa"
with pytest.raises(ValueError, match="Carga horaria invalida.*"):
        FabricaDisciplina.criar_disciplina("COD1", "Nome", 1, 50, "A")