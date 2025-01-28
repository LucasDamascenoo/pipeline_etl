#%%
import pandas as pd
from pyspark.sql import SparkSession
import requests
import io



# %% [markdown]

# Extract
# %%

url = 'http://compras.dados.gov.br/servicos/v1/servicos.csv?descricao=educação'
dados = requests.get(url).content
parse_data = io.StringIO(dados.decode('utf-8'))

df = pd.read_csv(parse_data)
# %%
type(df)

# %%
spark = SparkSession.builder.appName('aula01').getOrCreate()
# %%

# %%
df = spark.createDataFrame(df)

# %% [markdown]

# Transform

# %%

df = (df.withColumnRenamed("Código",'Codigo')
      .withColumnRenamed("Descrição","Descricao")
      .withColumnRenamed("Unidade medida","Unidade_medida")
      .withColumnRenamed("Seção","Secao")
      .withColumnRenamed("Divisão","Divisao")      
)

# %%
import pyspark.sql.functions as F
# %%
df = df.select([x.lower() for x in df.columns])
df.printSchema()
# %%
df.coalesce(1) \
    .write \
    .option("header", "true") \
    .mode("overwrite") \
    .csv("portal_transparencia.csv")
# %%

