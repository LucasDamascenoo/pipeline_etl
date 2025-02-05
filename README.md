# Api GitHub

Nesse projeto vamos criar uma pipeline para consumir dados de uma api (github) utilizando o request (biblioteca do python).

## Etapas do Projeto

1. criando o ambiente de desenvolvimento
2. Extraindo dados da Api
3. Transformando os dados 
4. Armazenando os dados

## Melhorias Criadas

 - Utilização do poetry para criar o ambiente de desenvolvimento 
 - Utilização do .dotenv para salvar a credencial da api

 ## Bibliotecas Utilizadas

 - Pandas
 - Requests
 - Os
 - Base64
 - dotEnv

## Desenvolvimento das etapas


**1.Criando o ambiente de desenvolvimento**

O curso foi passado o ambiente via Venv, mas conheco o poetry e fiz por ele.

1. instalamos o poetry: curl -sSL https://install.python-poetry.org | python3 -
2. adicionamos o executavel do poetry no {} settings.json "python.poetryPath": "$HOME/.local/bin/poetry" (coloque o caminho da onde esta salvo o seu poetry)
3. criamos um novo projeto: poetry new api-github
4. entramos no projeto cd new api-github e instalamos as dependencias que vamos usar (requests)

**2. Extraindo dados da Api**

Utilizando a biblioteca requests, fizemos a extracao dos dados da api do gitHub:


```{Python}:

headers = {'Authorization': 'Bearer ' + access_token,
           'X-GitHub-Api-Version': '2022-11-28'}

api_base_url = 'https://api.github.com'
owner = 'amzn' #username que vamos extrair os dados
url = f'{api_base_url}/users/{owner}/repos' #endopoint


```

- no codigo acima conseguimos puxar dados da api do github, mas trouxe apenas 30 repos, sendo que existem muito mais, isso se dar porque os demais repositorios estao em outras pagina/abas e para isso precisamos fazer a paginacao.

- Headers: eh utilizado para enviar mais informacaoes no request para que a resposta seja mais eficiente, como por exemplo o authorization que usamos para enviar nosso token

**Autenticacao**

Autenticacao e um processo de conferir o cliente(usuario) que esta tentando usar a api **cada api tem seu processo de autenticacao**.

- 1. acessar o nosso perfil no gitHub > settings > developer settings > personal acess token > token classic > new token > classic


**Não é uma boa prática salvar o token da sua API diretamente no código, pois isso pode expor sua chave a riscos de segurança. Para evitar esse problema, podemos usar a biblioteca dotenv, que permite armazenar o token em um arquivo .env e carregá-lo como uma variável de ambiente, mantendo a chave protegida.**


```{Python}:

import os
from dotenv import load_dotenv

# Obter o token de acesso da variável de ambiente
load_dotenv('/home/ubuntao/dev/pipeline_etl/api_git/.env') # Carrega as variáveis do .env

access_token = os.getenv("GITHUB_ACCESS_KEY")

```



**Paginacao**

processo de transitar entre paginas para extrair dados de cada pagina.


```{Python}:

repo_list = []

for page_num in range(1,7):
    try:
        url_page = f'{url}?page={page_num}'
        response = requests.get(url_page,headers=headers)
        repo_list.append(response.json())
    except:
        repo_list.append(None)

 for page in repo_list:
    for repo in page:
        repos_names.append(repo['name'])

repos_language = []

for page in repo_list: #percorrendo cada pagina da nossa lista
    for repo in page: # percorrendo cada repositorio da pagina
        repos_language.append(repo['language'])          

```

**3. Transformando os dados**

```{Python}:

dados_amz = pd.DataFrame({
    "repository_name": repos_names,
    "language_language": repos_language
})

dados_amz.to_csv('amazon.csv')
```

- o primeiro passo foi transformar nossas duas listas (repo_names e repos_language) em dataFrames

- em seguida salvamos as informações do DF em csv

**4. Armazenando os dados**

```{Python}:

api_base_url = 'https://api.github.com'
url = f'{api_base_url}/user/repos'

data = {
    'name': 'linguagem_utilizadas',
    'description':'Repositorio com as linguagens de prog da Amazon',
    'private': False

response = requests.post(url, json=data , headers=headers)
}
```

- Criamos um repositorio no nosso gitHub atraves do metodo HTTP post

```{Python}:

# convertendo csv  em binario(base64)

with open('amazon.csv','rb') as file:
    file_content = file.read()
    
    
encoded_content = base64.b64encode(file_content)

```

- em seguida transformamos o aruivo csv que salvamos anteriormente em binario(base64) para que ele seja capaz de ser enviado via put

```{Python}:

# subindo arquivo pro repositorio

api_base_url = 'https://api.github.com'
username = 'LucasDamascenoo'
repo = 'linguagem_utilizadas'
path = 'amazon.csv'
url = f'{api_base_url}/repos/{username}/{repo}/contents/{path}'

data = {
    'message': "Adicionando um novo arquivo",
    'content': encoded_content.decode('utf-8')}

```

- com o arquivo ja em binario, vamos atualizar nosso repositorio com a mensagem de commit e subir o arquivo csv.

[repositorio_criado](https://github.com/LucasDamascenoo/linguagem_utilizadas)



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