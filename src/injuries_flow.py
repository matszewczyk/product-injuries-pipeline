from datetime import datetime
from typing import List
import os

from prefect import flow, task
from src.pipelines.raw_to_staging_etl import injuries_etl
from src.transform_data import read_from_raw, clean_injuries_data
from src.pipelines.raw_to_staging_etl.common import SourceDataConfig

from minio import Minio

from collections import namedtuple

from src.pipelines.raw_to_staging_etl.injuries_etl import InjuriesETL
from src.pipelines.raw_to_staging_etl.products_etl import ProductsETL

if __name__ == '__main__':

    source_data_configs = [
        SourceDataConfig(
            "https://query.data.world/s/nfk36jyfu5zy4mrcrhh3md3ph6ttbf?dws=00000",
            ",",
            "raw/injuries.csv"
        ),
        SourceDataConfig(
            "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-product-codes/exports/csv",
            ";",
            "raw/products_mapping.csv"
        ),
    ]


    products_etl = ProductsETL(
        src_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-product-codes/exports/csv",
        raw_bucket_name= "injuries",
        raw_object_name="raw/products_mapping.csv",
        delimiter=";"
    )

    injuries_etl = InjuriesETL(
        src_url = "https://query.data.world/s/nfk36jyfu5zy4mrcrhh3md3ph6ttbf?dws=00000",
        raw_bucket_name= "injuries",
        raw_object_name="raw/injuries.csv",
        delimiter=","
    )

    products_etl.run()
    injuries_etl.run()




    # injuries_data_pipeline(
    #     trg_bucket_name = "injuries",
    #     source_data_configs = source_data_configs,
    #     trg_client = minio_client
    # )
