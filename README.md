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

## Síntese da elicitação

Com base nas discussões realizadas, relatos de professores e análise de sistemas semelhantes, a equipe identificou que a principal dificuldade na criação de grades universitárias está na organização manual dos horários, especialmente em relação a conflitos entre disciplinas e disponibilidade de professores.

A partir disso, foi definido que o sistema terá como foco auxiliar na geração e validação de grades horárias, buscando reduzir conflitos e facilitar a organização acadêmica de forma mais rápida e prática.

---

# Histórias de usuário

| ID   | História de usuário                                                                                                                                                      | Critérios de aceitação                                                                                                                                                        | Prioridade |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| HU01 | Como coordenador do curso, quero cadastrar as disciplinas ofertadas em cada período, para organizar quais turmas precisam ser consideradas na montagem da grade horária. | - Permite cadastrar nome da disciplina, período, carga horária e turma.<br>- Permite editar ou remover disciplinas cadastradas.<br>- Lista disciplinas por período.           | Alta       |
| HU02 | Como coordenador do curso, quero cadastrar os professores responsáveis por cada disciplina, para relacionar docentes às turmas que precisam de horário.                  | - Permite vincular professores a disciplinas.<br>- Impede disciplinas sem professor responsável.<br>- Exibe as disciplinas associadas a cada professor.                       | Alta       |
| HU03 | Como professor, quero informar meus horários disponíveis e indisponíveis, para que minhas restrições sejam consideradas na montagem da grade.                            | - Permite cadastrar horários disponíveis e indisponíveis.<br>- Salva as informações por semestre.<br>- Permite que o coordenador visualize essas informações.                 | Alta       |
| HU04 | Como professor, quero informar minhas preferências de horário, para que a coordenação possa considerá-las quando possível.                                               | - Permite indicar preferências de dias e horários.<br>- Diferencia restrições obrigatórias de preferências.<br>- Permite atualizar preferências antes do fechamento da grade. | Média      |
| HU05 | Como coordenador do curso, quero visualizar conflitos de horário entre professores, disciplinas e turmas, para corrigir problemas antes da publicação da grade.          | - Identifica professores alocados em horários simultâneos.<br>- Identifica conflitos entre disciplinas do mesmo período.<br>- Destaca conflitos encontrados.                  | Alta       |
| HU06 | Como coordenador do curso, quero gerar uma visualização preliminar da grade horária, para analisar a distribuição das aulas durante a semana.                            | - Exibe a grade organizada por dias e horários.<br>- Permite visualizar a grade por período/turma.<br>- Permite visualizar a grade por professor.                             | Alta       |
| HU08 | Como aluno, quero visualizar a grade horária do meu período, para saber quais disciplinas terei e em quais horários.                                                     | - Permite visualizar a grade por período.<br>- Exibe disciplina, professor, dia e horário.<br>- Disponibiliza a grade apenas após publicação pela coordenação.                | Média      |

---

# Registro da validação aplicada

Durante a análise das histórias de usuário, a equipe revisou os requisitos definidos para identificar ambiguidades e melhorar a clareza das funcionalidades propostas.

Foram ajustados critérios de aceitação que apresentavam inconsistências de escrita e também revisadas histórias relacionadas à organização dos horários e preferências dos professores, buscando deixar mais claro o comportamento esperado do sistema.

Além disso, a validação permitiu identificar requisitos que poderiam ampliar demais o escopo inicial da proposta, levando a equipe a priorizar funcionalidades consideradas essenciais para a primeira versão do sistema.

Esse processo ajudou a refinar os requisitos e reduzir ambiguidades nas histórias de usuário definidas para o projeto.
