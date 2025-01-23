#!/usr/bin/env python
# coding: utf-8



import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
#import wget

def main(params):
        user=params.user
        password=params.password
        host=params.host
        port=params.port
        db=params.db
        table_name=params.table_name
        url=params.url
        csv_name = 'output.csv'
        original_filename = os.path.basename(url)
        if not original_filename:
                original_filename = 'output.csv'

        csv_name = original_filename
        #download the csv
        # Download the file
        os.system(f"wget {url} -O {csv_name}")

        # Check if the file is compressed (.gz)
        is_compressed = csv_name.endswith('.gz')

        # Create a connection to the PostgreSQL database
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

        # Read the file in chunks for large datasets
        if is_compressed:
            df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip')
        else:
            df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
        
        df=next(df_iter)
        
        #change format from text to datetime
        # Check if 'tpep_pickup_datetime' column exists in the DataFrame
        if 'tpep_pickup_datetime' in df.columns:
                df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
                df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        # Check if 'lpep_pickup_datetime' column exists in the DataFrame
        elif 'lpep_pickup_datetime' in df.columns:
                df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
                df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

        # Handle the case where neither column exists
        else:
                print("Neither 'tpep_pickup_datetime' nor 'lpep_pickup_datetime' columns exist in the DataFrame.")            
        
        #input to sql only table column names
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        #insert first chunk of data (100k row) to sql database
        df.to_sql(name=table_name, con=engine, if_exists='append')

        #while there is data in chunks, input chunks to db
    # Insert remaining chunks (if any)
        while True:
            try:
                t_start = time()
                df = next(df_iter)

                # Convert datetime columns
                if 'tpep_pickup_datetime' in df.columns:
                    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
                    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
                elif 'lpep_pickup_datetime' in df.columns:
                    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
                    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
                else:
                    raise ValueError("Neither 'tpep_pickup_datetime' nor 'lpep_pickup_datetime' columns exist in the DataFrame.")

                # Insert the chunk
                df.to_sql(name=table_name, con=engine, if_exists='append')
                t_end = time()
                print('Inserted another chunk, took %.3f seconds' % (t_end - t_start))
            except StopIteration:
                print("All chunks processed.")
                break
            except Exception as e:
                print(f"Error processing chunk: {e}")
                break

        print("Data ingestion completed successfully.")




if __name__== '__main__':
        #make argument
        parser = argparse.ArgumentParser(
                        prog='Ingest CSV',
                        description='Ingest CSV Data to postgress',
                        epilog='test ingest csv')

        parser.add_argument('--user',help='username for postgres')           # positional argument
        parser.add_argument('--password',help='password for postgres')   
        parser.add_argument('--host',help='host for postgres')   
        parser.add_argument('--port',help='port for postgres')   
        parser.add_argument('--db',help='db name for postgres')   
        parser.add_argument('--table_name',help='name of table we will write')   
        parser.add_argument('--url',help='url of csv file')   

        args=parser.parse_args()
        print('args:')
        print(args)
        print('args_acc:')
       # print(args.accumulate(args.integers))
        main(args)


