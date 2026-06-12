import unittest
from Fabricas.fabrica_disciplina import FabricaDisciplina
from Fabricas.fabrica_professor import FabricaProfessor

class TestFabricaDisciplina(unittest.TestCase):

    def test_criar_disciplina_com_sucesso(self):
        # Sucesso: Instanciar com carga e período válidos
        disciplina = FabricaDisciplina.criar_disciplina("ES01", "Engenharia de Software", 2, 60)
        self.assertEqual(disciplina.codigo, "ES01")
        self.assertEqual(disciplina.carga_horaria, 60)
        self.assertEqual(disciplina.periodo, 2)

    def test_criar_disciplina_carga_horaria_invalida(self):
        # Falha: Carga horária não permitida (ex: 45h)
        with self.assertRaises(ValueError) as context:
            FabricaDisciplina.criar_disciplina("ES01", "Engenharia de Software", 2, 45)
        self.assertTrue("Carga horária inválida" in str(context.exception))

    def test_criar_disciplina_periodo_limite(self):
        # Borda: Período zero
        with self.assertRaises(ValueError) as context:
            FabricaDisciplina.criar_disciplina("ES01", "Engenharia de Software", 0, 60)
        self.assertTrue("período deve ser um número positivo" in str(context.exception).lower())


class TestFabricaProfessor(unittest.TestCase):

    def test_criar_professor_com_sucesso(self):
        # Sucesso: Nome válido com mais de 3 caracteres
        disponibilidade = {"Segunda": ["M1", "M2"]}
        professor = FabricaProfessor.criar_professor(1, "Silva", disponibilidade)
        self.assertEqual(professor.nome, "Silva")
        self.assertEqual(professor.id_prof, 1)

    def test_criar_professor_nome_vazio(self):
        # Falha: Nome vazio
        disponibilidade = {"Segunda": ["M1", "M2"]}
        with self.assertRaises(ValueError) as context:
            FabricaProfessor.criar_professor(1, "", disponibilidade)
        self.assertTrue("inválido" in str(context.exception).lower())

    def test_criar_professor_nome_limite(self):
        # Borda: Nome com apenas 2 caracteres ou apenas espaços
        disponibilidade = {"Segunda": ["M1", "M2"]}
        
        # Testando 2 caracteres
        with self.assertRaises(ValueError):
            FabricaProfessor.criar_professor(1, "Ed", disponibilidade)
            
        # Testando apenas espaços
        with self.assertRaises(ValueError):
            FabricaProfessor.criar_professor(2, "   ", disponibilidade)

if __name__ == '__main__':
    unittest.main()