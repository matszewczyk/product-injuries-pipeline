
import pandas as pd
from prefect import flow, task

from src.pipelines.raw_to_staging_etl.common import SourceDataConfig
from src.pipelines.raw_to_staging_etl.raw_to_staging_etl import RawToStagingETL

SourceDataConfig(
    "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/us-national-electronic-injury-surveillance-system-neiss-product-codes/exports/csv",
    ";",
    "raw/products_mapping.csv"
)


class ProductsETL(RawToStagingETL):

    @task(name='products-transform')
    def transform(seld, df: pd.DataFrame) -> pd.DataFrame:
        return df