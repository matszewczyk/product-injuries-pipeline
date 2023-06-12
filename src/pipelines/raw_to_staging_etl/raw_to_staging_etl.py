import os 
import pandas as pd
from prefect import task, flow
from src.pipelines.raw_to_staging_etl.common import SourceDataConfig, get_df_from_url, save_df_to_raw

from minio import Minio

class RawToStagingETL:
    minio_client = Minio(
        endpoint='127.0.0.1:9000',
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False
    )

    def __init__(
            self, src_url: str, raw_bucket_name: str, raw_object_name: str, 
            delimiter: str = ",", encoding: str = "utf-8"
        ):
            self.src_url = src_url
            self.delimiter = delimiter
            self.encoding = encoding

            self.raw_bucket_name = raw_bucket_name
            self.raw_object_name = raw_object_name

    @flow
    def run(self):
        df = self.extract()
        df = self.transform(df)
        self.load(df)

    @task
    def extract(self):
        df = get_df_from_url(self.src_url, self.delimiter)
        save_df_to_raw(df, RawToStagingETL.minio_client, self.raw_bucket_name, self.raw_object_name, self.encoding)
        return df

    @task
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    @task
    def load(self, df: pd.DataFrame):
        pass
