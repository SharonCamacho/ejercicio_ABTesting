from google.cloud import bigquery
import os

from config import *

def load_data(df_results):
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("exp_name", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("variant_id", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("date", bigquery.enums.SqlTypeNames.STRING),
        ],
        write_disposition="WRITE_TRUNCATE",
    )
    job = client.load_table_from_dataframe(df_results, table_id, job_config=job_config)  
    job.result() 
    table = client.get_table(table_id)  
    return  "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id)
    