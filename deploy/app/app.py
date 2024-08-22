#Importo librerías
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
import pandas as pd
import logging
from google.cloud import bigquery
import os

from config import *

#Creo la app
app = FastAPI()

# Configuro el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Creo raíz
@app.get("/")
def leer_raiz():
    return {"mensaje": "AB testing Sharon Camacho"}

#Defino extracción de experimento
@app.get("/experiment/{exp_id}/result")
def get_experiment_result(exp_id: int, day: str = Query(...)):
    """Extrae un experimento de la forma 
        experiment/<:id>/result?day=YYYY-MM-DD HH
        
       Entrega un json de la forma
       results: { exp_name : {
                    number_of_participants : NNN
                    winner: variant_id
                    variants : [{
                        id: 1
                        number_of_purchases: 100
                        }]
                    }
                }"""
    
    logger.info(f"Received request for experiment {exp_id} on day {day}")
    try: 
        # Filtro los datos según la petición del usuario
        table = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"
        print(table)
        query = f"""SELECT * 
        FROM `{table}` 
        WHERE exp_id={exp_id} and date = '{day}'
        ORDER BY purchases DESC"""
        print(query)
        print(PROJECT_ID)
        client = bigquery.Client(project=PROJECT_ID)
        job_config = bigquery.QueryJobConfig()
        exp_data = client.query(query, job_config=job_config).to_dataframe()
        logger.debug(f"Filtered data shape: {exp_data.shape}")
        #Creo la excepción si no encuentra el experimiento
        if exp_data.empty:
            logger.warning(f"No data found for experiment {exp_id} on day {day}")
            raise HTTPException(status_code=404, detail="Experimento no encontrado")
        # Convierto los datos en el formato requerido
        results = {}
        for exp_name, exp_group in exp_data.groupby('exp_name'):
            results[exp_name] = {
                'number_of_participants': int(exp_group['participants'].sum()),  # Convertir a int
                'winner': int(exp_group['variant_id'].iloc[0]),  # Convertir a int
                'variants': [
                    {'id': int(variant_id),  # Convertir a int
                     'number_of_purchases': int(exp_group[exp_group['variant_id'] == variant_id]['purchases'].sum())}  # Convertir a int
                    for variant_id in exp_group['variant_id'].unique()
                ]
            }
        # Creo la llave "results" para guardar los resultados
        response_data = {'results': results}
        # Retorno el resultado 
        return JSONResponse(content=response_data)
    except ValueError as ve:
        logger.error(f"Invalid date format: {str(ve)}")
        raise HTTPException(status_code=400, detail="Invalid date format.")
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

