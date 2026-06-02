# Documentação dos padrões de codificação e gestão / qualidade

## Padrões de codificação

O projeto será desenvolvido em Python utilizando convenções baseadas na PEP8, buscando manter organização, legibilidade e padronização do código.

As principais práticas adotadas pela equipe são:

- Utilização de nomes descritivos para variáveis, funções, classes e arquivos;
- Uso de nomes em português para manter consistência com a proposta do projeto;
- Utilização de funções e módulos com responsabilidades específicas;
- Comentários apenas quando necessários para explicar regras de negócio ou trechos importantes do sistema;

---

## Organização do projeto

O sistema será organizado em módulos separados de acordo com suas responsabilidades:

- `modelos/`: entidades principais do sistema;
- `servicos/`: regras de negócio e lógica da aplicação;
- `fabricas/`: criação de objetos utilizando o padrão Factory;
- `repositorios/`: armazenamento e organização dos dados;
- `testes/`: testes automatizados do sistema.

Essa separação busca facilitar manutenção, reutilização e entendimento do código.

Exemplo visual:

codigo/
│
├── main.py
│
├── modelos/
│ ├── professor.py
│ ├── disciplina.py
│ ├── horario.py
│ └── grade_horaria.py
│
├── servicos/
│ ├── gerador_grade.py
│ ├── validador_conflitos.py
│ └── organizador_horarios.py
│
├── fabricas/
│ ├── fabrica_professor.py
│ ├── fabrica_disciplina.py
│ └── fabrica_horario.py
│
├── repositorios/
│ ├── repositorio_professores.py
│ ├── repositorio_disciplinas.py
│ └── repositorio_horarios.py
│
├── utils/
│ └── formatadores.py
│
└── testes/
├── teste_conflitos.py
└── teste_gerador.py

---

## Gestão e qualidade

Para auxiliar na organização e qualidade do projeto, a equipe definiu as seguintes práticas:

- Utilização do GitHub para versionamento do código;
- Divisão de responsabilidades entre os integrantes;
- Refinamento contínuo dos requisitos durante as sprints e com feedback do professor;

## Diagrama de arquitetura dos componentes

### Diagrama visual

Usuário
↓

main.py
↓

servicos/

↓

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
