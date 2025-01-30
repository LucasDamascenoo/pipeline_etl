#%%
import requests
# %%
# estamos fazendo uma requisiçao (é uma solicitaçao para um servidor)
# cliente > request > servidor
# servidor > response > cliente
dados = requests.get('https://api.github.com/versions')
dados_lucas = requests.get('https://api.github.com/users/LucasDamascenoo')
dados.json()
# %%


# %%
dados.status_code #verfica o status code
dados.url # mostra a url passada
dados.text # retorna o conteudo da api como string
dados.json() # retorna o conteudo da api em json
dados_lucas.status_code
dados_lucas.json()['public_repos']
dados_lucas.json()['created_at']
dados_lucas.json()['login']
dados_lucas.json()['name']
dados_lucas.json()
# %%
api_base_url = 'https://api.github.com'
owner = 'amzn' #username que vamos extrair os dados

url = f'{api_base_url}/users/{owner}/repos' #endopoint
# %%
response = requests.get(url)
response.json()