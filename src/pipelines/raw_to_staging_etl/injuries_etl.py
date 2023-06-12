from prefect import flow, task
import pandas as pd

from src.pipelines.raw_to_staging_etl.common import SourceDataConfig
from src.pipelines.raw_to_staging_etl.raw_to_staging_etl import RawToStagingETL

SourceDataConfig(
    "https://query.data.world/s/nfk36jyfu5zy4mrcrhh3md3ph6ttbf?dws=00000",
    ",",
    "raw/injuries.csv"
)

class InjuriesETL(RawToStagingETL):

    @task(name="injuries-transform")
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[df['age'] != 0]
        df['treatmentDate'] = pd.to_datetime(df['treatmentDate'])
        df = df[df['race'].notna()]
        return df