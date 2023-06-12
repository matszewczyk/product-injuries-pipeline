from io import BytesIO, StringIO
import pandas as pd
from collections import namedtuple

SourceDataConfig = namedtuple("SourceDataConfig", ["src_url", "delimiter", "trg_object_name"])

def get_df_from_url(
        src_url: str, 
        delimiter: str = ","
    ):
    df = pd.read_csv(src_url, delimiter=delimiter)
    return df

def save_df_to_raw(
        df: pd.DataFrame,
        trg_client,
        trg_bucket_name: str,
        trg_object_name: str,
        encoding: str = "utf-8"
    ):
    csv_bytes = df.to_csv().encode(encoding)
    csv_buffer = BytesIO(csv_bytes)
    
    return trg_client.put_object(
        bucket_name=trg_bucket_name,
        object_name=trg_object_name,
        data=csv_buffer,
        length=len(csv_bytes),
        content_type='application/csv'
    )

def read_from_raw(minio_client, bucket_name: str, object_name: str):
    response = minio_client.get_object(bucket_name, object_name)
    data = response.data.decode('utf-8')
    df = pd.read_csv(StringIO(data), index_col=0)
    return df
