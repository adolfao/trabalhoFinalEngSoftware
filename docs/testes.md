# Estratégia de Testes

A estratégia adotada para este projeto foca em testes de unidade voltados para a validação de integridade dos dados no momento de criação dos objetos. Como o sistema lida com restrições acadêmicas estritas de alocação de horários e carga horária, garantir que as entidades do domínio não sejam instanciadas com dados inválidos é o passo mais crítico. Utilizaremos a biblioteca `unittest` nativa do Python para automatizar esses testes nas classes do padrão *Factory*, que funcionam como a barreira de segurança e validação do sistema.

## Adequação e Lacunas Não Cobertas

Essa estratégia é adequada ao escopo atual pois isola e protege o domínio da aplicação, garantindo estabilidade antes que os dados cheguem aos repositórios ou ao algoritmo gerador de grade. 

Por outro lado, optou-se por não realizar testes de integração ou testes de interface (E2E) nesta etapa. Consequentemente, o funcionamento do menu interativo no terminal, a persistência no arquivo JSON e a exibição visual da grade gerada não estão cobertos por testes automatizados, sendo validados apenas por testes manuais exploratórios durante o desenvolvimento.

## Casos de Teste (Unittest)

Foram selecionados dois métodos críticos das fábricas para a implementação dos testes automatizados, garantindo a cobertura dos três cenários exigidos (sucesso, falha e borda):

### 1. Método: `FabricaDisciplina.criar_disciplina()`
* **Sucesso:** Instanciar uma disciplina com carga horária válida (ex: 60) e período válido (ex: 2).
* **Falha:** Tentar instanciar uma disciplina com carga horária não mapeada na grade (ex: 45), esperando o levantamento da exceção `ValueError`.
* **Borda:** Testar o limite da restrição do período, passando o valor limite `0`, esperando o levantamento da exceção `ValueError`.

### 2. Método: `FabricaProfessor.criar_professor()`
* **Sucesso:** Instanciar um professor com um nome válido contendo mais de 3 caracteres.
* **Falha:** Tentar instanciar um professor passando uma string vazia (`""`) no nome, esperando o levantamento da exceção `ValueError`.
* **Borda:** Tentar instanciar um professor com um nome no limite da validação, contendo exatamente 2 caracteres (ex: "Ed") ou apenas espaços em branco (`"   "`), esperando o levantamento da exceção `ValueError`.
