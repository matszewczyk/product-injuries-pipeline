from typing import Callable
from prefect import flow
from raw_data_pipeline import etl
from raw_data_pipeline.transformers import injuries
from raw_data_pipeline.transformers import products

from minio import Minio
import os

@flow(flow_run_name="{raw_object_name}")
def etl_flow(src_url: str, 
    raw_bucket_name: str, 
    raw_object_name: str,
    src_delimiter: str,
    transfomer: Callable
):

    df = etl.extract_from_url(src_url, src_delimiter)
    etl.load_to_raw(df, raw_bucket_name, raw_object_name)
    df = transfomer(df)
    etl.load(df)


if __name__ == '__main__':
    src_url = "https://query.data.world/s/nfk36jyfu5zy4mrcrhh3md3ph6ttbf?dws=00000"
    src_delimiter=","
    raw_bucket_name= "injuries"
    raw_object_name="raw/injuries.csv"

    etl_flow(src_url, raw_bucket_name, raw_object_name, src_delimiter, injuries.transform)

    src_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-product-codes/exports/csv"
    src_delimiter=";"
    raw_bucket_name= "injuries"
    raw_object_name="raw/products_mapping.csv"

    etl_flow(src_url,  raw_bucket_name, raw_object_name, src_delimiter, products.transform)
