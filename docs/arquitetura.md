# Documentação dos padrões de codificação e gestão / qualidade

## Padrões de codificação

O projeto será desenvolvido em Python, seguindo convenções baseadas na PEP 8 para manter o código organizado, legível e padronizado.

As funções, variáveis e arquivos serão nomeados em `snake_case`, utilizando letras minúsculas e separação por underline. Exemplos:

```python
gerar_grade_horaria()
verificar_disponibilidade()
carga_horaria_professor
modelo_alocacao.py
```

As classes serão nomeadas em `PascalCase`, com a primeira letra de cada palavra em maiúscula. Exemplos:

```python
Professor
Turma
HorarioAula
ModeloAlocacao
```

As constantes serão escritas em letras maiúsculas, também separadas por underline. Exemplos:

```python
MAXIMO_AULAS_DIA = 7
HORARIOS_REUNIAO = ["M4", "M5"]
```

Os nomes utilizados no código serão, preferencialmente, em português e descritivos, evitando abreviações ou nomes genéricos como `aux`, `var1` ou `funcao1`.

O código será dividido em funções e módulos com responsabilidades específicas, como carregamento de dados, criação do modelo, definição das restrições e exportação dos resultados.

A indentação seguirá o padrão de 4 espaços por nível. Os comentários serão utilizados apenas quando necessários para explicar regras de negócio ou trechos importantes do sistema.

---

## Organização do projeto

O sistema será organizado em módulos separados de acordo com suas responsabilidades:

- `modelos/`: entidades principais do sistema;
- `servicos/`: regras de negócio e lógica da aplicação;
- `fabricas/`: criação de objetos utilizando o padrão Factory;
- `repositorios/`: armazenamento e organização dos dados;
- `testes/`: testes automatizados do sistema.

Essa separação busca facilitar manutenção, reutilização e entendimento do código.

### Exemplo visual

```txt
codigo/
│
├── main.py                # Ponto de entrada do sistema
│
├── data/                  # Armazenamento persistente
│   └── entities.json
│
├── Modelos/               # Entidades de negócio (Dominio)
│   ├── __init__.py
│   ├── professor.py
│   ├── disciplina.py
│   └── vinculo.py
│
├── Repositorios/          # Gestão de coleções em memória
│   ├── __init__.py
│   ├── repositorio_professores.py
│   ├── repositorio_disciplinas.py
│   └── repositorio_vinculos.py
│
├── Servicos/              # Regras de negócio e persistência
│   ├── __init__.py
│   ├── interface_usuario.py
│   ├── persistencia.py    # Serviço de I/O para o JSON
│   ├── gerador_grade.py
│   └── validador_conflitos.py
│
├── Fabricas/              # Padrão Factory para instâncias
│   ├── __init__.py
│   ├── fabrica_professor.py
│   └── fabrica_disciplina.py
│
└── testes/                # Testes automatizados
    └── ...
```

---

## Gestão e qualidade

Para auxiliar na organização e qualidade do projeto, a equipe definiu as seguintes práticas:

- Utilização do GitHub para versionamento do código;
- Divisão de responsabilidades entre os integrantes;
- Refinamento contínuo dos requisitos durante as sprints e com feedback do professor;

## Diagrama de arquitetura dos componentes

### Diagrama visual

```txt
Usuário
   ↓

main.py
   ↓

servicos/
├── gerador_grade.py
├── validador_conflitos.py
└── organizador_horarios.py

   ↓

modelos/
├── professor.py
├── disciplina.py
├── horario.py
└── grade_horaria.py

   ↓

repositorios/
├── repositorio_professores.py
├── repositorio_disciplinas.py
└── repositorio_horarios.py
```

### Explicação de responsabilidades

main.py
Controla o fluxo do sistema.

servicos/
Onde fica a lógica principal.

modelos/
Representa os dados.

repositorios/
Controla armazenamento e acesso aos dados.

Todos utilizam a fabrica/ e o utils/

## Trade-offs adotados

### Arquitetura em Camadas

Prós:
Melhor organização do sistema, separação de responsabilidades e maior facilidade de manutenção do código.

Contras:
Maior quantidade de arquivos e necessidade de mais organização da equipe.

Justificativa:
A equipe escolheu essa arquitetura para separar melhor as partes do sistema e deixar o código mais organizado e modular.

---

### Armazenamento em memória

Prós:
Desenvolvimento mais simples, menor complexidade inicial e maior facilidade para testes.

Contras:
Os dados não permanecem salvos após encerrar a aplicação.

Justificativa:
A equipe decidiu não utilizar banco de dados na primeira versão para focar primeiro na lógica principal do sistema.

---

### Escopo reduzido

Prós:
Maior foco nas funcionalidades principais, menor risco de funcionalidades incompletas e maior viabilidade dentro do prazo da disciplina.

Contras:
Algumas funcionalidades ficaram planejadas para versões futuras.

Justificativa:
A equipe priorizou as funcionalidades relacionadas à organização e validação da grade horária para manter o projeto mais viável e consistente.


## Padrões de Projeto Aplicados

Para garantir a manutenibilidade, extensibilidade e a separação de responsabilidades do sistema, foram aplicados intencionalmente dois padrões de projeto consagrados pelo GoF (Gang of Four): **Factory Method** (Criacional) e **Strategy** (Comportamental).

----

### 1. Padrão Criacional: Factory Method

#### Justificativa e Aplicabilidade
A criação das entidades de grade envolve validações de consistência estrita antes do objeto ser aceito na memória. Centralizamos essa lógica em fábricas na pasta fabricas/. Se o terminal receber uma carga horária inválida (diferente de 30, 60 ou 90) ou um período negativo, a fábrica barra a criação imediatamente.

#### Diagrama de Classes
```txt
+-----------------------------+
|      FabricaEntidade        | <--- (Interface/Classe Abstrata)
+-----------------------------+
| + criar_entidade()          |
+-----------------------------+
               ▲
               | (Herança)
      +--------+--------+
      |                 |
+-----------------+ +-------------------+
| FabricaProfessor| | FabricaDisciplina |
+-----------------+ +-------------------+
| + criar()       | | + criar()         |
+-----------------+ +-------------------+
        |                     |
        v (Instancia)         v (Instancia)
+-----------------+ +-------------------+
|    Professor    | |    Disciplina     |
+-----------------+ +-------------------+
```

### 2. Padrão Comportamental: Strategy

### Justificativa e Aplicabilidade
O maior desafio do sistema é a identificação de conflitos (HU05). Em vez de criar uma sequência massiva de blocos if/else difíceis de testar, isolamos cada regra de validação académica numa classe Strategy independente dentro de servicos/validador_conflitos.py.

O contexto ValidadorConflitos apenas varre uma lista de estratégias ativas. Se amanhã a coordenação exigir uma nova regra (ex: "limite de 4 horas de aula seguidas para o mesmo período"), basta criar uma nova classe que implemente a interface, sem tocar no código que já funciona.

```txt
+------------------------------------------------------------------+
 |                       ValidadorConflitos                         |
 |                           (Contexto)                             |
 +------------------------------------------------------------------+
 | - _estrategias: List[EstrategiaValidacao]                        |
 +------------------------------------------------------------------+
 | + executar_validacoes(grade: GradeHoraria) -> List[str]          |
 +------------------------------------------------------------------+
                                  |
                                  | o-- [Agrega e executa 1..n]
                                  v
 +------------------------------------------------------------------+
 |                    <<interface / ABC>>                           |
 |                    EstrategiaValidacao                           |
 +------------------------------------------------------------------+
 | + validar(grade: GradeHoraria) -> List[str]                      |
 +------------------------------------------------------------------+
                                  ▲
                                  | (Implementação das Regras)
         +------------------------+------------------------+
         |                                                 |
 +----------------------------------+     +----------------------------------+
 |       ValidaChoqueDocente        |     |       ValidaChoquePeriodo        |
 +----------------------------------+     +----------------------------------+
 | # Verifica se o mesmo professor  |     | # Impede que duas disciplinas do |
 | # está em duas salas no mesmo    |     | # mesmo período/turma tenham     |
 | # dia e horário.                 |     | # aulas sobrepostas.             |
 +----------------------------------+     +----------------------------------+
 | + validar(grade) -> List[str]    |     | + validar(grade) -> List[str]    |
 +----------------------------------+     +----------------------------------+
```
