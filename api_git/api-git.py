#%%
import pandas as pd
import base64
import requests
import os
from dotenv import load_dotenv,dotenv_values
# %%
# estamos fazendo uma requisiçao (é uma solicitaçao para um servidor)
# cliente > request > servidor
# servidor > response > cliente

# Carregar variáveis de ambiente do arquivo .env
load_dotenv('/home/ubuntao/dev/pipeline_etl/api_git/.env') # Carrega as variáveis do .env

access_token = os.getenv("GITHUB_ACCESS_KEY")


# %%

# %%
headers = {'Authorization': 'Bearer ' + access_token,
           'X-GitHub-Api-Version': '2022-11-28'}

api_base_url = 'https://api.github.com'
owner = 'amzn' #username que vamos extrair os dados
url = f'{api_base_url}/users/{owner}/repos' #endopoint


# %% [markdown]
## Paginacao

#%%
repo_list = []

for page_num in range(1,7):
    try:
        url_page = f'{url}?page={page_num}'
        response = requests.get(url_page,headers=headers)
        repo_list.append(response.json())
    except:
        repo_list.append(None)        


# %% [markdown]

## Transformacao
# %%

#Selecionando os nomes dos repositorios
repo_list[5][1]['name']

repos_names = []

for page in repo_list:
    for repo in page:
        repos_names.append(repo['name'])
        
# %%

#Selecionando as linguagens dos repositorios

repos_language = []

for page in repo_list: #percorrendo cada pagina da nossa lista
    for repo in page: # percorrendo cada repositorio da pagina
        repos_language.append(repo['language'])     



# %% [markdown]

### Criando DataFrame


# %%

dados_amz = pd.DataFrame({
    "repository_name": repos_names,
    "language_language": repos_language
})

dados_amz.to_csv('amazon.csv')
# %%

# Criando repositorio via post

api_base_url = 'https://api.github.com'
url = f'{api_base_url}/user/repos'

data = {
    'name': 'linguagem_utilizadas',
    'description':'Repositorio com as linguagens de prog da Amazon',
    'private': False
}

response = requests.post(url, json=data , headers=headers)

# %%

# convertendo csv  em binario(base64)

with open('amazon.csv','rb') as file:
    file_content = file.read()
    
    
encoded_content = base64.b64encode(file_content)

# subindo arquivo pro repositorio

api_base_url = 'https://api.github.com'
username = 'LucasDamascenoo'
repo = 'linguagem_utilizadas'
path = 'amazon.csv'
url = f'{api_base_url}/repos/{username}/{repo}/contents/{path}'

data = {
    'message': "Adicionando um novo arquivo",
    'content': encoded_content.decode('utf-8')
    
}


response = requests.put(url,json=data, headers=headers)

response.status_code


