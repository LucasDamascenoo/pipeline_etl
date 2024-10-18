# pipeline_etl

Nesse projeto vamos criar uma pipeline para consumir dados de uma api (github) utilizando o request.



## Etapas do Projeto

1. criando o ambiente de desenvolvimento
2. compreendendo sobre os metodos http,o que sao request e response
3. Extraindo dados da Api

## Desenvolvimento das etapas


**1.Criando o ambiente de desenvolvimento**

O curso foi passado o ambiente via Venv, mas conheco o poetry e fiz por ele.

1. instalamos o poetry: curl -sSL https://install.python-poetry.org | python3 -
2. adicionamos o executavel do poetry no {} settings.json "python.poetryPath": "$HOME/.local/bin/poetry" (coloque o caminho da onde esta salvo o seu poetry)
3. criamos um novo projeto: poetry new api-github
4. entramos no projeto cd new api-github e instalamos as dependencias que vamos usar (requests)

**2. compreendendo sobre os metodos http,o que sao request e response**

- Métodos do http: Get: responsavel por obter dados de uma requiçao

**3. Extraindo dados da Api**

