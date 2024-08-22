import datetime
import pandas as pd
import plotly.graph_objects as go
import pytz

from modulos.cleaning import *
from modulos.bigquery import *

#Se carga el archivo
url = "https://drive.google.com/file/d/1mzY4SYyh-VJneRTF7zc-8PgYatQRQnX8/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
data = pd.read_csv(path)
#Se formatean las fechas
df = cleaning_dates(data)
#Se organizan los datos por usuario fecha y hora
df = df.sort_values(by=['user_id','fecha', 'hora'])
#Se crea una llave para identificar los eventos
df['key'] = df['user_id'].astype(str) + df['item_id'].astype(str)
df.reset_index(inplace=True)
df.drop(columns='index',inplace=True)
#Se crean campos auxiliares
df = create_fields(df)
#Selecciono las llaves de los eventos que fueron compra 
items_buyed = df[df['event_name']=='BUY'].key.unique()
#Se limpian los registros
df = clean_cases(df, items_buyed)
#Se extrae el detalle del experimento
df = clean_experiments(df)
#Se preprocesa el dataframe
df_pre = preprocesing(df)
#Se realiza conteo de comprar y participante por experimento fecha y variante
df_results = df_pre.groupby(['exp_name','variant_id','date']).agg({'purchases':'sum','participants':'sum'}).reset_index()
df_results['exp_id'] = df_results.groupby('exp_name').ngroup() + 1
#Se guarda el ID de los experimentos
tabla_exp = df_results[['exp_name','exp_id']].value_counts().reset_index()
tabla_exp = tabla_exp[['exp_name','exp_id']]
#tabla_exp.to_csv('tabla_exp.csv', index=False)}

# Se Carga la data en Bigquery
print(load_data(df_results))

