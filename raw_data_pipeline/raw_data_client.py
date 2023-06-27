import os 
from minio import Minio
import pandas as pd

from io import BytesIO, StringIO

CLIENT = Minio(
    endpoint='127.0.0.1:9000',
    access_key=os.getenv('MINIO_ACCESS_KEY'),
    secret_key=os.getenv('MINIO_SECRET_KEY'),
    secure=False
)

def read_df_from_raw(bucket_name: str, object_name: str):
    response = CLIENT.get_object(bucket_name, object_name)
    data = response.data.decode('utf-8')
    df = pd.read_csv(StringIO(data), index_col=0)
    return df

def write_df_to_raw(df: pd.DataFrame, trg_bucket_name: str, trg_object_name: str, encoding: str = "utf-8") -> bool:
    
    csv_bytes = df.to_csv().encode(encoding)
    csv_buffer = BytesIO(csv_bytes)

    return CLIENT.put_object(
        bucket_name=trg_bucket_name,
        object_name=trg_object_name,
        data=csv_buffer,
        length=len(csv_bytes),
        content_type='application/csv'
    )
