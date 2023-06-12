import os
from io import StringIO

from prefect import task
import pandas as pd

@task
def prepare_db():
    pass

@task
def read_from_raw(minio_client, bucket_name: str, object_name: str):
    response = minio_client.get_object(bucket_name, object_name)
    data = response.data.decode('utf-8')
    df = pd.read_csv(StringIO(data), index_col=0)
    return df

@task
def clean_injuries_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['age'] != 0]
    df['treatmentDate'] = pd.to_datetime(df['treatmentDate'])
    df = df[df['race'].notna()]
    return df
