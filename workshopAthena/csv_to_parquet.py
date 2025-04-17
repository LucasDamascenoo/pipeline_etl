# %%
import pandas as pd
import os
import pyarrow as pa  # para trabalhar com parquet
import pyarrow.parquet as pq
import boto3


def process_csv(csv_file: str, output_dir: str, bucket_name: str, s3_key: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    s3 = boto3.client('s3')

    df = pd.read_csv(csv_file)

    json_file = os.path.join(
        output_dir, 'Netflix_movies_and_tv_shows_clustering.json')

    df.to_json(json_file, orient='records', lines=False)

    parquet_file = os.path.join(
        output_dir, "Netflix_movies_and_tv_shows_clustering.parquet")

    table = pa.Table.from_pandas(df)

    pq.write_table(table, parquet_file)

    s3.upload_file(parquet_file, bucket_name, s3_key)
