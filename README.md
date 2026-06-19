# Sistema de Gestão de Grade Universitária

## Infos Gerais

### Integrantes

- Adolfo
- Isabelle Rosvadoski Nofre
- Daniel Carvalho

---

## Descrição do problema

Um sistema que auxilia coordenadores universitários na criação e organização de grades horárias, considerando disponibilidade de professores, disciplinas e possíveis conflitos de horário.

O sistema busca reduzir o tempo gasto na montagem manual das grades e diminuir conflitos entre disciplinas e docentes.

---

## Público-alvo

- Coordenadores de curso
- Secretarias acadêmicas
- Instituições de ensino superior

---

## Fontes utilizadas

- Relatos e experiências compartilhadas por professores universitários sobre dificuldades na montagem manual de grades horárias.
- Um modelo de programação matemática para o problema de atribuição dos horários de aulas dos professores de um curso:
  https://repositorio.utfpr.edu.br/jspui/handle/1/37395

---

## Divisão de Responsabilidades

## Divisão de Responsabilidades

| Membro                    | Responsabilidades iniciais                                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Isabelle Rosvadoski Nofre | Documentação do projeto, estruturação da proposta, criação das histórias de usuário e definição dos critérios de aceitação.                |
| Adolfo                    | Elicitação de requisitos, análise de sistemas similares, validação das histórias de usuário e apoio no desenvolvimento inicial do sistema. |
| Daniel                    | Organização da estrutura do sistema, apoio na modelagem das funcionalidades e auxílio na validação dos requisitos definidos pela equipe.   |

---

# Roteiro e síntese da elicitação

## Método utilizado

A equipe realizou discussões sobre os principais problemas enfrentados na montagem manual de grades universitárias, como conflitos de horário e dificuldade na organização das disciplinas. Também foram utilizados relatos de professores universitários e análise de sistemas acadêmicos semelhantes, como SIGAA e SUAP, para entender melhor o problema e possíveis funcionalidades do sistema.

A partir dessas análises, foram definidos os requisitos iniciais e o foco principal da aplicação.

---

## Principais problemas identificados

- Dificuldade em organizar horários sem conflitos
- Processo manual demorado
- Dependência excessiva do coordenador
- Possibilidade de choque entre disciplinas e professores
- Dificuldade de ajustar mudanças na grade

---

## Necessidades identificadas

- Cadastro de professores e disciplinas
- Registro da disponibilidade dos professores
- Verificação automática de conflitos
- Geração mais rápida da grade horária
- Facilidade para realizar alterações futuras

---

## Como executar

Pré-requisitos: Python 3.10+.

```bash
# (opcional) instalar o solver de otimização
pip install -r Codigos/requirements.txt

# gerar a grade a partir de um arquivo de entrada
cd Codigos
python main.py entrada.json            # método de otimização (padrão)
python main.py entrada.json heuristica # método heurístico
```

O sistema **recebe um arquivo JSON** como entrada (professores, disciplinas e
vínculos), gera a grade horária e imprime o relatório no terminal — sem
interface interativa.

### Formato da entrada

```json
{
  "professores": [
    {"id_prof": 1, "nome": "Luiz",
     "disponibilidade": {"Terca": ["T1", "T2"]},
     "preferencias": ["Sexta"]}
  ],
  "disciplinas": [
    {"codigo": "ENCO6A", "nome": "Engenharia de Software",
     "periodo": 6, "carga_horaria": 60, "turma": "A"}
  ],
  "vinculos": [
    {"id_prof": 1, "codigo": "ENCO6A"}
  ],
  "salas": ["Sala A", "Sala B"]
}
```

> A chave `salas` é opcional: se omitida, o sistema assume uma sala por período.

---

## Decisões de projeto

- **Arquitetura em camadas** (`modelos`, `servicos`, `fabricas`, `repositorios`)
  para separar responsabilidades.
- **Factory Method** (`fabricas/`): centraliza a validação na criação das entidades.
- **Strategy** em dois pontos: validação de conflitos (`validador_conflitos.py`)
  e geração da grade (heurística vs. otimização MILP).
- **Modelo matemático**: a geração por otimização reproduz o modelo de alocação do
  TCC de referência (UTFPR Apucarana), considerando disponibilidade dos professores,
  choque de docente, choque de período (uma turma por período), turno por paridade
  do período, máximo de aulas por dia e **alocação de salas** (locais físicos: uma
  sala não recebe duas aulas no mesmo horário).
- **Armazenamento em memória**: sem banco de dados nesta versão.
