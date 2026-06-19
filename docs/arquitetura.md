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
Codigos/
│
├── main.py                     # Ponto de entrada (leitura e relatório)
├── entrada.json                # Entrada estruturada
├── requirements.txt            # Dependências (PuLP)
│
├── modelos/
│   ├── professor.py
│   ├── disciplina.py
│   ├── horario.py
│   └── grade_horaria.py
│
├── servicos/
│   ├── leitor_entrada.py       # Leitura JSON
│   ├── gerador_grade.py        # Heurística gulosa
│   ├── gerador_grade_otimizado.py # MILP (PuLP)
│   ├── validador_conflitos.py
│   └── organizador_horarios.py
│
├── fabricas/
│   ├── fabrica_professor.py
│   ├── fabrica_disciplina.py
│   └── fabrica_horario.py
│
├── repositorios/
│   ├── repositorio_professores.py
│   ├── repositorio_disciplinas.py
│   └── repositorio_vinculos.py
│
└── testes/                     # Testes automatizados (pytest)
    ├── test_leitor.py
    ├── test_fabricas.py
    └── test_repositorios.py
---

## Gestão e qualidade

Para auxiliar na organização e qualidade do projeto, a equipe definiu as seguintes práticas:

- Utilização do GitHub para versionamento do código;
- Divisão de responsabilidades entre os integrantes;
- Refinamento contínuo dos requisitos durante as sprints e com feedback do professor;

## Diagrama de arquitetura dos componentes

### Diagrama visual

```txt
Arquivo de entrada (entrada.json)
   ↓

main.py
   ↓

servicos/
├── leitor_entrada.py
├── gerador_grade.py / gerador_grade_otimizado.py
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
└── repositorio_vinculos.py
```

### Explicação de responsabilidades

main.py
Controla o fluxo: le o arquivo de entrada, aciona o gerador escolhido e imprime o relatorio da grade.

servicos/
Onde fica a lógica principal (leitura da entrada, geração da grade, validação de conflitos e organização da saída).

modelos/
Representa os dados.

repositorios/
Controla armazenamento e acesso aos dados (em memória).

Os serviços e repositórios utilizam as entidades criadas pelas fabricas/.

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

Atualmente há três estratégias de validação: `ValidaChoqueDocente` (mesmo professor em dois lugares ao mesmo tempo), `ValidaChoquePeriodo` (duas disciplinas do mesmo período/turma no mesmo horário) e `ValidaChoqueSala` (uma sala — local físico — com duas aulas no mesmo horário). Cada alocação da grade guarda também a `sala` em que ocorre.

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
 | # está em duas turmas no mesmo   |     | # mesmo período/turma tenham     |
 | # dia e horário.                 |     | # aulas sobrepostas.             |
 +----------------------------------+     +----------------------------------+
 | + validar(grade) -> List[str]    |     | + validar(grade) -> List[str]    |
 +----------------------------------+     +----------------------------------+
```

#### Segundo uso do Strategy: geradores de grade

A geração da grade também usa Strategy. A interface `GeradorGradeStrategy`
(`servicos/gerador_grade_base.py`) define o método `gerar(vinculos)`, e há duas
estratégias concretas e intercambiáveis:

- `GeradorGrade` — heurística gulosa (rápida, encontra *uma* grade válida);
- `GeradorGradeOtimizado` — otimização linear inteira (MILP) com o solver CBC via
  PuLP, reproduzindo o modelo matemático do TCC de referência (maximiza alocação
  e preferências de dia respeitando todas as restrições).

O `main.py` escolhe a estratégia conforme o método informado, sem conhecer os
detalhes de cada algoritmo.

```txt
        <<interface / ABC>> GeradorGradeStrategy
                  + gerar(vinculos) -> GradeHoraria
                                ▲
              +-----------------+-----------------+
              |                                   |
        GeradorGrade                     GeradorGradeOtimizado
        (heurística gulosa)              (otimização MILP / PuLP)
```

#### Trade-off: heurística vs. otimização

A heurística não tem dependências externas e é instantânea, mas não garante a
melhor grade. A otimização (PuLP) encontra a solução ótima da função objetivo,
ao custo de uma dependência externa (`pulp`). Mantivemos as duas como estratégias
para permitir a comparação e demonstrar o padrão Strategy; a otimização é o
método padrão e a heurística é o fallback quando o PuLP não está instalado.


#### Estratégia de Qualidade e Testes

Para garantir a confiabilidade do sistema, adotamos uma estratégia baseada na Pirâmide de Testes.

1. Resumo da Execução
A bateria de testes foi implementada via pytest e valida os métodos críticos de Entrada, Domínio e Estado.

- Total de casos de teste: 7
- Status atual: 100% PASSED.

2. Mapeamento de Métodos Testados

================================================================================
*MAPEAMENTO DE MÉTODOS TESTADOS*
================================================================================

*Classe / Módulo*          | *Método(s) Testado(s)*    | *Cenários (Sucesso/Falha/Borda)*
--------------------------------------------------------------------------------
LeitorEntrada            | ler()                  | Validação de JSON, vínculos e default.
FabricaDisciplina        | criar_disciplina()     | Regras de negócio (carga horária).
RepositorioProfessores   | adicionar() / remover()| Gestão de estado, ID e inexistentes.
--------------------------------------------------------------------------------

O *LeitorEntrada* lida com o mundo externo, que é imprevisível. As *Fábricas* lidam com as regras de negócio, que não podem ser violadas.
E os *Repositórios* lidam com a integridade dos dados em memória

*Validação da Entrada (LeitorEntrada.ler):* Este método atua como o "porteiro" do seu software. Se ele falhar em interpretar o JSON ou permitir que dados inconsistentes entrem, todo o restante do sistema (geração de grade, validação de conflitos) operará sobre uma base corrompida. Testar o fluxo de sucesso, falha e borda aqui garante que o sistema seja resiliente a arquivos mal formatados ou incompletos.

*Validação de Regras de Negócio (FabricaDisciplina.criar_disciplina):* As fábricas funcionam como a "camada de blindagem" das regras de negócio. Ao testar se a fábrica rejeita cargas horárias fora do padrão (ex: 50h), estamos provando que o sistema é capaz de impor restrições acadêmicas automaticamente, sem depender de validações externas ou manuais.

*Integridade do Estado (RepositorioProfessores.adicionar/remover):* O repositório é onde a "memória" do seu sistema reside enquanto ele está aberto. Testar o comportamento de adição e remoção garante que, durante a execução, o software não sofra com bugs de memória, como IDs duplicados ou referências perdidas, o que é essencial para manter a grade coerente durante toda a sessão de uso.

3. Análise Crítica: Estratégia vs. Lacunas

*- Adequação:* A abordagem de testes unitários isola falhas e facilita refatorações.

*- Lacunas:* Módulos de alto nível (GeradorGrade e ValidadorConflitos) possuem cobertura limitada devido à complexidade algorítmica, sendo alvo de testes de integração em iterações futuras.
