from typing import Callable
from prefect import flow
from data_pipeline.raw_etl import etl
from data_pipeline.raw_etl.transformers import injuries, products

from prefect_airbyte.server import AirbyteServer
from prefect_airbyte.connections import AirbyteConnection
from prefect_airbyte.flows import run_connection_sync
from prefect_dbt import DbtCoreOperation

AIRBYTE_SERVER = AirbyteServer(server_host="localhost", server_port=8000)

@flow(flow_run_name="{raw_object_name}", log_prints=True)
def etl_flow(src_url: str, 
    raw_bucket_name: str, 
    raw_object_name: str,
    src_delimiter: str,
    raw_transfomer: Callable,
    airbyte_connection_id: str,
):

    df = etl.extract_from_url(src_url, src_delimiter)
    etl.load_to_raw(df, raw_bucket_name, raw_object_name)
    df = raw_transfomer(df)
    etl.load(df)
    
    connection = AirbyteConnection(
        airbyte_server=AIRBYTE_SERVER,
        connection_id=airbyte_connection_id, #"injuries_data_from_minio_to_postgres",
        status_updates=True,
    )
    
    run_connection_sync(
        airbyte_connection=connection,
    )
    
    dbt_build_op = DbtCoreOperation.load("dbt-build-block")
    dbt_build_op.run()


if __name__ == '__main__':
    src_url = "https://query.data.world/s/nfk36jyfu5zy4mrcrhh3md3ph6ttbf?dws=00000"
    src_delimiter=","
    raw_bucket_name= "injuries"
    raw_object_name="raw/injuries.csv"
    airbyte_connection_id="780c9e24-bb86-439a-9ff1-a34bf69e4b5d"

    etl_flow(src_url, raw_bucket_name, raw_object_name, src_delimiter, injuries.transform, airbyte_connection_id)

    src_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-product-codes/exports/csv"
    src_delimiter=";"
    raw_bucket_name= "injuries"
    raw_object_name="raw/products_mapping.csv"
    airbyte_connection_id="7eb7ad8a-5487-4424-88a5-528000438ab0"

    etl_flow(src_url,  raw_bucket_name, raw_object_name, src_delimiter, products.transform, airbyte_connection_id)
