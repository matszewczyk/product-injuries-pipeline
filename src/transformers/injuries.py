import pandas as pd
from prefect import task

@task
def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['age'] != 0]
    df['treatmentDate'] = pd.to_datetime(df['treatmentDate'])
    df = df[df['race'].notna()]
    return df