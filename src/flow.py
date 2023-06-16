from typing import Callable
from prefect import flow
from src import etl
from src.transformers import injuries
from src.transformers import products

from minio import Minio
import os

raw_client = Minio(
    endpoint='127.0.0.1:9000',
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False
)


@flow(flow_run_name="{raw_object_name}")
def flow(
    src_url, 
    raw_client, 
    raw_bucket_name, 
    raw_object_name,
    delimiter,
    transfomer: Callable
):

    df = etl.extract_from_url(src_url, delimiter)
    etl.save_to_raw(df, raw_client, raw_bucket_name, raw_object_name)
    df = transfomer(df)
    etl.load(df)


if __name__ == '__main__':
    src_url = "https://query.data.world/s/nfk36jyfu5zy4mrcrhh3md3ph6ttbf?dws=00000"
    raw_bucket_name= "injuries"
    raw_object_name="raw/injuries.csv"
    delimiter=","

    flow(src_url, raw_client, raw_bucket_name, raw_object_name, delimiter, injuries.transform)

    src_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-product-codes/exports/csv"
    raw_bucket_name= "injuries"
    raw_object_name="raw/products_mapping.csv"
    delimiter=";"

    flow(src_url, raw_client, raw_bucket_name, raw_object_name, delimiter, products.transform)