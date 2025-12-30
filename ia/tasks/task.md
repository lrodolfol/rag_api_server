<critical>
***Não me peça permissão para alterar arquivo por arquivo. Faça a alteração em todos arquivos que for necessário e somente depois me pergunte se pode seguir com todas as alterações de uma única vez.***
</critical>

## Idioma
Todo o código-fonte deve ser escrito em inglês, incluindo nomes de variáveis, funções, classes, comentários e documentação.

## Nomenclatura Clara
Evite abreviações, mas também não escreva nomes muito longos (com mais de 30 caracteres).

## Métodos e Funções
Os métodos e funções devem executar uma ação clara e bem definida, e isso deve ser refletido no seu nome, que deve começar por um verbo, nunca um substantivo.
Metodos e funções sempre devem informar seu retorno mesmo que seja none

## Senhas e dados sensiveis
Nunca coloque dados sensiveis como senhas, codigos e token no código. Todas deverão ser armazenadas em variaveis de ambiente
Nunca coloque dados de confingurações diretamente no código. Todas deverão ser armazenadas em arquivos de configuração dentro da pasta ./configuration nos aquivos config.dev.yml ou config.prod.yml e devem ser lidas pela classe ./static/Settings.py

## Parâmetros
Sempre que possível, evite passar mais de 3 parâmetros. Dê preferência para o uso de objetos caso necessário.

## Funções
Evite passar e retornar variaveis nulos. Preencha com valores default ou use exceções.

## Tratamento de Erros e Exceções
Se lançar uma exceção, sempre emita um log claro do erro usando o logger ./static/LogginService.py

## Tamanho de Métodos e Classes
- Evite métodos longos, com mais de 50 linhas
- Evite classes longas, com mais de 300 linhas

## Comentários
Evite o uso de comentários sempre que possível. O código deve ser autoexplicativo.

## Variaveis
Evite criar variaveis e propriedades sem tipo. Procure criar variaveis e propriedade com seu tipo.
**Exemplo:**
```python
// ❌ Evite
name = "Carl"
Create(name){}

// ✅ Prefira
name: str = "Carl"
Create(name: str){}
```