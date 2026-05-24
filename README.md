# Resolução Grade universitária

## Infos Gerais

### Integrantes

Adolfo, Isabelle e ...

### Descrição do problema

Um sistema que auxilia coordenadores universitários na criação de grades horárias automaticamente, considerando disponibilidade de professores, horários das disciplinas e possíveis conflitos.

### Público alvo

Coordenadores de curso, secretarias acadêmicas e instituições de ensino superior

### Fonte real

Um modelo de programação matemática para o problema de atribuição dos horários de aulas dos professores de um curso:
https://repositorio.utfpr.edu.br/jspui/handle/1/37395

### Divisão de Responsabilidades

| Membro                    | Responsabilidades iniciais                                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Isabelle Rosvadoski Nofre | Documentação do projeto, estruturação da proposta, criação das histórias de usuário e definição dos critérios de aceitação.                |
| Adolfo                    | Elicitação de requisitos, análise de sistemas similares, validação das histórias de usuário e apoio no desenvolvimento inicial do sistema. |

## Roteiro e síntese da elicitação

A equipe realizou discussões sobre os principais problemas enfrentados na montagem manual de grades universitárias, como conflitos de horário e dificuldade na organização das disciplinas. Também foi feita uma análise de sistemas semelhantes e de um TCC relacionado ao tema, com o objetivo de entender possíveis soluções e funcionalidades úteis para o sistema.

A partir dessas análises, foram definidos os requisitos iniciais e o foco principal da aplicação.

### Principais problemas identificados

Dificuldade em organizar horários sem conflitos
Processo manual demorado
Dependência excessiva do coordenador
Possibilidade de choque entre disciplinas e professores
Dificuldade de ajustar mudanças na grade
Problemas pessoais entre coordenador e professor

### Necessidades identificadas

Cadastro de professores e disciplinas
Registro da disponibilidade dos professores
Verificação automática de conflitos
Geração mais rápida da grade horária
Facilidade para realizar alterações futuras

### Síntese da elicitação

Com base nas discussões realizadas e na análise de sistemas semelhantes, a equipe identificou que a principal dificuldade na criação de grades universitárias está na organização manual dos horários, especialmente em relação a conflitos entre disciplinas e disponibilidade de professores.

A partir disso, foi definido que o sistema terá como foco auxiliar na geração e validação de grades horárias, buscando reduzir conflitos e facilitar a organização acadêmica de forma mais rápida e prática.

## Histórias de usuário

| ID | História de usuário | Critérios de aceitação | Prioridade |
|---|---|---|---|
| HU01 | Como coordenador do curso, quero cadastrar as disciplinas ofertadas em cada período, para organizar quais turmas precisam ser consideradas na montagem da grade horária. | - Deve ser possível cadastrar nome da disciplina, período, carga horária e turma. <br> - O sistema deve permitir editar ou remover uma disciplina cadastrada. <br> - O sistema deve listar as disciplinas por período. | Alta |
| HU02 | Como coordenador do curso, quero cadastrar os professores responsáveis por cada disciplina, para relacionar docentes às turmas que precisam de horário. | - Deve ser possível vincular um professor a uma ou mais disciplinas. <br> - O sistema deve impedir que uma disciplina fique sem professor responsável. <br> - O sistema deve exibir quais disciplinas estão associadas a cada professor. | Alta |
| HU03 | Como professor, quero informar meus horários disponíveis e indisponíveis, para que minhas restrições sejam consideradas na montagem da grade. | - O professor deve conseguir marcar horários disponíveis e indisponíveis. <br> - O sistema deve salvar as informações por semestre. <br> - O coordenador deve conseguir visualizar essas informações. | Alta |
| HU04 | Como professor, quero informar minhas preferências de horário, para que a coordenação possa considerá-las quando possível. | - O professor deve conseguir indicar preferências de dias e horários. <br> - O sistema deve diferenciar restrições obrigatórias de preferências. <br> - O sistema deve permitir atualizar as preferências antes do fechamento da grade. | Média |
| HU05 | Como coordenador do curso, quero visualizar conflitos de horário entre professores, disciplinas e turmas, para corrigir problemas antes da publicação da grade. | - O sistema deve identificar quando um professor está alocado em dois horários ao mesmo tempo. <br> - O sistema deve identificar conflitos entre disciplinas do mesmo período. <br> - O sistema deve destacar os conflitos encontrados. | Alta |
| HU06 | Como coordenador do curso, quero gerar uma visualização preliminar da grade horária, para analisar a distribuição das aulas durante a semana. | - O sistema deve exibir a grade organizada por dias e horários. <br> - Deve ser possível visualizar a grade por período/turma. <br> - Deve ser possível visualizar a grade por professor. | Alta |
| HU07 | Como coordenador do curso, quero registrar observações sobre decisões tomadas na montagem da grade, para manter um histórico das escolhas realizadas. | - O sistema deve permitir adicionar observações em disciplinas, professores ou horários. <br> - As observações devem ficar salvas junto à versão da grade. <br> - O coordenador deve conseguir consultar essas observações posteriormente. | Média |
| HU08 | Como aluno, quero visualizar a grade horária do meu período, para saber quais disciplinas terei e em quais horários. | - O sistema deve permitir visualizar a grade por período. <br> - A visualização deve mostrar disciplina, professor, dia e horário. <br> - A grade deve estar disponível apenas após a publicação pela coordenação. | Média |
| HU09 | Como coordenador do curso, quero publicar a versão final da grade, para que professores e alunos tenham acesso aos horários definidos. | - O sistema deve permitir marcar uma grade como finalizada. <br> - Após a publicação, a grade deve ficar visível para alunos e professores. <br> - Alterações posteriores devem ser registradas como nova versão ou atualização. | Alta |
