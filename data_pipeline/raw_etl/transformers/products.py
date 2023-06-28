import pandas as pd
from prefect import task

@task
def transform(df: pd.DataFrame) -> pd.DataFrame:
    return df