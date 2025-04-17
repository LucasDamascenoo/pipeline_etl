# %%
from csv_to_parquet import process_csv


def main():
    csv_file = '/home/ubuntao/dev/pipeline_etl/workshopAthena/data/Netflix_movies_and_tv_shows_clustering.csv'
    output_dir = 'workshopAthena/output_file'
    bucket_name = 'sql-athena-parquet-lucas'
    s3_key = 'parquet_files/workshopAthena/data/Netflix_movies_and_tv_shows_clustering.parquet'

    process_csv(csv_file, output_dir, bucket_name, s3_key)


if __name__ == "__main__":
    main()

# %%
