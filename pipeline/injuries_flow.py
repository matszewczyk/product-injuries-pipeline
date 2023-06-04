from datetime import datetime
from typing import List
import os

from prefect import flow, task
from regex import F
from pipeline.extract_raw_data import get_df_from_url, save_df_to_raw

from minio import Minio

from collections import namedtuple


SourceDataConfig = namedtuple("SourceDataConfig", ["src_url", "delimiter", "trg_object_name"])

@flow(
    flow_run_name="extract {trg_object_name}"
)
def extract(
    src_url: str, 
    trg_bucket_name: str,
    trg_object_name: str,
    trg_client,
    delimiter: str = ",",
    encoding: str = "utf-8"
):
    df = get_df_from_url(src_url, delimiter)
    save_df_to_raw(df, trg_client, trg_bucket_name, trg_object_name, encoding)

@flow(
    flow_run_name="Injuries-on-{date:%A}"
)
def injuries_flow(
    trg_bucket_name: str,
    trg_client,
    source_data_configs: List[SourceDataConfig],
    date: datetime = datetime.utcnow(),
):
    """
    The Injuries Data Pipeline
    """
    # extract_args = []
    # for i, config in enumerate(source_data_configs):
    #     extract_args.append((
    #         config.src_url, config.trg_object_name, config.delimiter,
    #         trg_bucket_name, trg_client,
    #     ))
    
    # extract.map(extract_args)

    for config in source_data_configs:
        extract(
            src_url=config.src_url,
            trg_object_name=config.trg_object_name,
            delimiter=config.delimiter,
            trg_bucket_name=trg_bucket_name,
            trg_client=trg_client,
            )

if __name__ == '__main__':

    minio_client = Minio(
        endpoint='127.0.0.1:9000',
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False
    )

    source_data_configs = [
        SourceDataConfig("https://query.data.world/s/nfk36jyfu5zy4mrcrhh3md3ph6ttbf?dws=00000", ",", "raw/injuries.csv"),
        SourceDataConfig(
            "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-product-codes/exports/csv",
            ";",
            "raw/products_mapping.csv"
        ),
    ]

    injuries_flow(
        trg_bucket_name = "injuries",
        source_data_configs = source_data_configs,
        trg_client = minio_client
    )
