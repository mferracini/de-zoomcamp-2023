import argparse
import os
from time import time
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
import numpy as np
import pandas as pd



NYC_TAXI_DATA_URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
NYC_TAXI_DIM_URL="https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"

## download data
def download_from_url(url: str, output_path: str) -> None:
    os.system("wget -O {0} {1}".format(output_path, url))

## create tables
def create_table(df: pd.DataFrame, table_name: str, engine: Engine) -> None:
    create_statement = pd.io.sql.get_schema(df, name=table_name, con=engine)
    print(create_statement)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

## insert data
def insert_data_from_df(df, table_name: str, engine: Engine, chunksize=100000):
    if chunksize > df.shape[0]:
        df.to_sql(name=table_name, con=engine, if_exists="append")
    else:    
        n_splits = int(df.shape[0]/chunksize)
        split_dfs = np.array_split(df, n_splits)
        for split_df in split_dfs:
            split_df.to_sql(name=table_name, con=engine, if_exists="append")
            print(f"{split_df.shape[0]} rows inserted.")

def main(params):

    start_pipeline = time()
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    table_name = params.table_name
    db = params.db
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    metadata_obj = MetaData()
    tables = metadata_obj.sorted_tables

    if table_name in tables:
        if_exists_action = params.if_exists        #action if table alredy existr
        if if_exists_action == "skip":
            return "table already exists. Skiping insert."

    #download files only if they do not exist
    if not os.path.exists("data/ny_taxi"):
        os.mkdir("./data/ny_taxi/")

    if params.url == "trips":
        path = "data/ny_taxi/yellow_tripdata_2021-01.parquet"
        if not os.path.isfile(path):
            download_from_url(NYC_TAXI_DATA_URL, path)
        df = pd.read_parquet(path)

    elif params.url == "zone":
        path = "data/ny_taxi/taxi_zone.csv"
        if not os.path.isfile(path):
            download_from_url(NYC_TAXI_DIM_URL, "data/ny_taxi/taxi_zone.csv")
        df = pd.read_csv(path)

    
    create_table(df=df, table_name=table_name, engine=engine)
    print("Table Created Succesfully!")

    insert_data_from_df(df=df, table_name=table_name, engine=engine, chunksize=100000)
    print("Data Inserted Succesfully!")

    finish_pipeline = time()
    pipeline_time = finish_pipeline = start_pipeline
    print(f"Pipeline finished in {pipeline_time:.3f} seconds")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Ingestion of data into Postgres db.")
    parser.add_argument('--user', help='postgres user')
    parser.add_argument('--password', help='postgres password')
    parser.add_argument('--host', help='postgres host')
    parser.add_argument('--port', help='postgres port')
    parser.add_argument('--db', help='postgres db')
    parser.add_argument('--table_name', help='postgres table name where we will persist data')
    parser.add_argument('--url', help='url to download data from')
    parser.add_argument("--if_exists", help="action to take if table already exists", nargs='?', type=str, default="skip")

    args = parser.parse_args()
    print(args)
    main(args)