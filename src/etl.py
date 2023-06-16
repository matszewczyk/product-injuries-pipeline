import pandas as pd
from prefect import task
from src.common import get_df_from_url, save_df_to_lake

@task
def extract_from_url(src_url: str, delimiter: str):
    df = get_df_from_url(src_url, delimiter)
    return df

@task
def save_to_raw(df: pd.DataFrame, raw_client, raw_bucket_name, raw_object_name):
    save_df_to_lake(df, raw_client, raw_bucket_name, raw_object_name)

@task
def load(df: pd.DataFrame):
    pass