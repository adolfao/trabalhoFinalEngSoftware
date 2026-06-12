# Síntese da elicitação

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
| HU07 | Como aluno, quero visualizar a grade horária do meu período, para saber quais disciplinas terei e em quais horários.                                                     | - Permite visualizar a grade por período.<br>- Exibe disciplina, professor, dia e horário.<br>- Disponibiliza a grade apenas após publicação pela coordenação.                | Média      |

---

# Registro da validação aplicada

Durante a análise das histórias de usuário, a equipe revisou os requisitos definidos para identificar ambiguidades e melhorar a clareza das funcionalidades propostas.

Foram ajustados critérios de aceitação que apresentavam inconsistências de escrita e também revisadas histórias relacionadas à organização dos horários e preferências dos professores, buscando deixar mais claro o comportamento esperado do sistema.

Além disso, a validação permitiu identificar requisitos que poderiam ampliar demais o escopo inicial da proposta, levando a equipe a priorizar funcionalidades consideradas essenciais para a primeira versão do sistema.

Esse processo ajudou a refinar os requisitos e reduzir ambiguidades nas histórias de usuário definidas para o projeto.
