from io import BytesIO
import pandas as pd
from prefect import task, get_run_logger


@task
def get_df_from_url(
        src_url: str, 
        delimiter: str = ","
    ):
    df = pd.read_csv(src_url, delimiter=delimiter)
    get_run_logger().info(f"Reading the data from: {src_url}.")
    return df

@task
def save_df_to_raw(
        df: pd.DataFrame,
        trg_client,
        trg_bucket_name: str,
        trg_object_name: str,
        encoding: str = "utf-8"
    ):
    csv_bytes = df.to_csv().encode(encoding)
    csv_buffer = BytesIO(csv_bytes)
    
    get_run_logger().info(f"Saving the data: {trg_object_name}.")
    return trg_client.put_object(
        bucket_name=trg_bucket_name,
        object_name=trg_object_name,
        data=csv_buffer,
        length=len(csv_bytes),
        content_type='application/csv'
    )