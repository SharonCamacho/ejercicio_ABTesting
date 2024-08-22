import pandas as pd

def cleaning_dates(df):
    """
    Limpia y transforma las columnas de fechas y horas en un DataFrame.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['fecha'] = df['timestamp'].dt.date
    df['hora'] = df['timestamp'].dt.strftime('%H:%M:%S')  
    df['zona_horaria'] = df['timestamp'].dt.strftime('%z') 
    df['timestamp'] = df['timestamp'].dt.floor('S')
    return df

def create_fields(df):
    """
    Crea nuevas columnas en el DataFrame para almacenar eventos 
    y claves previos y siguientes.
    """
    #Almaceno los datos previos y siguientes para algunas columnas
    df['prev_event'] = df['event_name'].shift(+1)
    df['prev_key'] = df['key'].shift(+1)
    df['prev_exp'] = df['experiments'].shift(+1)
    df['next_user_id'] = df['user_id'].shift(-1)
    #Valida si un registro tiene el mismo valor del registro anterior
    df['val_exp'] = df['prev_exp'] == df['experiments']
    return df

def clean_cases(df,items_buyed):
    """
    Limpia los casos en el DataFrame añadiendo una columna que 
    valida si hubo compra y calculando la diferencia en minutos 
    entre eventos.
    """
    #creo una columna donde se valida si hubo compra o no
    df['val_buy'] = df['key'].isin(items_buyed)
    df['next_val_buy'] = df['val_buy'].shift(-1)
    #Para los items el evento search que no tiene item_id se le agrega el del evento siguiente
    df.loc[(df['user_id'] == df['next_user_id']) & (df['next_val_buy'] == True), 'val_buy'] = True
    #Se calcula la diferencia en minutos entre un evento y el siguiente
    df['diff_minutes'] = df['timestamp'].diff().dt.total_seconds() / 60
    #Se eliminan las filas que tengan el mismo experimento y una diferencia 
    # de menos de un minuto porque sería datos duplicados
    df = df[
        ~((df['event_name'] == df['prev_event']) & 
        (df['diff_minutes'] < 1) &
        (df['val_exp']==True)
        )
    ]
    return df

def clean_experiments(df):
    """
    Limpia y reorganiza la información de experimentos en el DataFrame.
    """
    # Se extraen los experimentos
    df_exp = df['experiments'].str.replace('{','').str.replace('}','').str.split(', ', expand=True)
    #Se contatena el dataframe con los experimentos
    df = pd.concat([df, df_exp], axis=1)
    #Se convierte la info de los experimentos de columnas a filas
    df = pd.melt(df, id_vars=['user_id', 'fecha', 'hora', 'item_id',
                              'event_name','experiments', 'timestamp', 'site',
                              'zona_horaria', 'key', 'next_user_id', 'val_buy',
                              'next_val_buy'], value_vars=[0, 1, 2, 3, 4, 5, 6, 7,
                                                           8, 9, 10, 11, 12, 13, 
                                                           14, 15, 16, 17, 18],
                            var_name='Variable', value_name='exp')
    #Se Extrae del experimento el nombre y la variante
    df_exp_var = df.exp.str.split('=', expand=True)
    df = pd.concat([df, df_exp_var], axis=1)
    #Renombramiento de columnas
    df.columns = ['user_id', 'fecha', 'hora', 'item_id', 'event_name',  
                'experiments', 'timestamp', 'site', 'zona_horaria',
                'key', 'next_user_id', 'val_buy', 'next_val_buy', 
                'Variable', 'exp','experiment_name', 'variant_id']
    #Se eliminan los experimentos nulos que queda por la conversión de columnas a filas
    df = df.dropna(subset=['experiment_name'])
    #Limpieza de columnas y se rellenan nulos
    df = df[['user_id', 'fecha', 'hora', 'item_id', 'event_name', 
        'timestamp', 'site', 'zona_horaria', 'key', 'val_buy',
            'experiment_name', 'variant_id']]
    df['item_id'].fillna(-199999, inplace=True)
    df = df.sort_values(by=['user_id','fecha', 'hora'])
    df.reset_index(inplace=True)
    return df

def preprocesing(df):
    """
    Realiza el procesamiento final de datos para análisis, incluyendo conteo de experimentos y pivotación.
    """
    #Se realiza conteo de experimentos
    df = df.groupby(['event_name','experiment_name','variant_id',
                        'timestamp','user_id','item_id','val_buy']).size().reset_index(name='counts')
    #Se pivotea para crear una columna que diferencia de compras True/False
    df = df.pivot_table(
        index=['event_name', 'experiment_name','variant_id', 'timestamp', 'user_id', 'item_id'],
        columns='val_buy',
        aggfunc='size',
        fill_value=0
    ).reset_index()
    #Renombramiento
    df.columns = ['event_name', 'exp_name',  'variant_id',     'date',
                'user_id', 'item_id', 'no_purchases', 'purchases']
    #Se calculan participantes
    df['participants'] = df['no_purchases'] + df['purchases']
    df.drop(columns='no_purchases',inplace=True)
    #Se formatea la fecha según requerimiento para API
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H')
    return df