# Orientações de Qualidade do Projeto

Este documento resume as práticas e critérios de qualidade para o projeto.

1. Estrutura e nomenclatura
   - Use apenas nomes de diretórios e pacotes em minúsculas (`modelos`, `fabricas`, `servicos`).
   - Evite caracteres acentuados em nomes de arquivos e pastas para garantir portabilidade.
   - Inclua `__init__.py` em pacotes quando desejar compatibilidade explícita com pacotes Python.

2. Código e estilo
   - Siga o estilo PEP8: linhas <= 79 caracteres, indentação de 4 espaços.
   - Use nomes claros e em português para variáveis e métodos quando o domínio for em português.
   - Tipagem: adicione anotações de tipo sempre que possível (`typing`).

3. Organização de responsabilidades
   - Separe modelos (entidades), fábricas (criação) e serviços (regras/validações).
   - Código de domínio no pacote `modelos`, lógica de negócio em `servicos` e fábricas em `fabricas`.

4. Testes e validação
   - Adicione testes unitários para cada regra de validação (pasta `tests/`).
   - Testes devem ser auto-contidos e independentes.

5. Documentação
   - Atualize `docs/requisitos.md` e `docs/arquitetura.md` sempre que houver mudança de contrato ou arquitetura.
   - Inclua exemplos de uso em `Codigos/main.py` como demonstração.

6. Gestão de erros
   - Lance exceções claras (`ValueError`, `TypeError`) com mensagens informativas.
   - Sempre capture exceções em pontos de entrada (e.g., `main.py`) para registrar/mostrar erros amigáveis.

7. Portabilidade
   - Evite dependências que exijam configurações específicas de SO.
   - Teste execução básica em Windows, Linux e Mac quando possível.

8. Commits e histórico
   - Mensagens de commit claras: `Área: ação - descrição curta` (ex.: `servicos: adicionar validador de conflitos`).
