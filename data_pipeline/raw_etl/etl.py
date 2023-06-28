import pandas as pd
from prefect import task
from data_pipeline.raw_etl.raw_data_client import write_df_to_raw

@task
def extract_from_url(src_url: str, src_delimiter: str):
    df = pd.read_csv(src_url, delimiter=src_delimiter)
    return df

@task
def load_to_raw(df: pd.DataFrame, raw_bucket_name, raw_object_name):
    write_df_to_raw(df, raw_bucket_name, raw_object_name)

@task
def load(df: pd.DataFrame):
    pass