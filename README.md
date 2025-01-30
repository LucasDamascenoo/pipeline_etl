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



# Portal da Transparencia

## Etapas do Projeto

1. extrair dados publicos, de compras orcamentais
2. tratar os dados
3. Armazenar os dados

## Desenvolvimento de cada etapa

**1. extrair dados publicos, de compras orcamentais**

Atraves da biblioteca requests, fizemos uma requisicao na API do governo que tras dados de compras orcamentais.

```{Python}:

url = 'http://compras.dados.gov.br/servicos/v1/servicos.csv?descricao=educação'
dados = requests.get(url).content
parse_data = io.StringIO(dados.decode('utf-8'))

df = pd.read_csv(parse_data)


```

**url**: define uma url que aponta um csv do portal de transparencia, que possui parametro a educacao.
**dados**: usamos o request.get(queremos buscar os dados). content (onde definimos que queremos os dados brutos)

**parse_data**: transformamos o retorn dos dados (byte) em uma string que nos permite tranformar os dados em um df posteriormente

**df**: utilizamos o pandas para transformar em um dataFrame

**2. tratar os dados**

Fizemos nossos tratamentos (coisa simple) com o spark, para isso criarmos uma **spark.Session**

```{Python}:

spark = SparkSession.builder.appName('aula01').getOrCreate()

df = spark.createDataFrame(df)


```

**spark**: criarmos uma sparkSession para podermos usar as funcoes do spark
**df**: transformarmos o df (pandas) em df(spark)


**Renomeamos as colunas com acentos para sem acentos e em seguida transformamos columa em minusculo**
```{Python}:

df = (df.withColumnRenamed("Código",'Codigo')
      .withColumnRenamed("Descrição","Descricao")
      .withColumnRenamed("Unidade medida","Unidade_medida")
      .withColumnRenamed("Seção","Secao")
      .withColumnRenamed("Divisão","Divisao")      
)

df = df.select([x.lower() for x in df.columns])

```

**3. Armazenar os dados**

Apos as pequenas mudancas acima, salvamos os dados em csv.

```{Python}:
df.coalesce(1) \
    .write \
    .option("header", "true") \
    .mode("overwrite") \
    .csv("portal_transparencia.csv")

```

- white : indica que vamos realizar uma operacao de escrita
- option: indicamos que queremos cabecalhos (colunas)
- mode :  indicamos o comportamento, caso  o destino/arquivo ja exista(se tiver vai excluir o anterior e salvar o novo)
- csv:  indicamos o formato e o nome do arquivo