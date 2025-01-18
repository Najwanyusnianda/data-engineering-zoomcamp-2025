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
        csv_name = 'output.csv.gz'
        
        #download the csv
        os.system(f"wget {url} -O {csv_name}")
        
        
        
        #df=pd.read_csv('yellow_tripdata_2021-01.csv',nrows=200)
        engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        #print(pd.io.sql.get_schema(df,name='yellow_taxi_data',con=engine))
        
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000, compression='gzip')
        
        df=next(df_iter)
        
        #change format from text to datetime
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        #input to sql only table column names
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        #insert first chunk of data (100k row) to sql database
        df.to_sql(name=table_name, con=engine, if_exists='append')

        #while there is data in chunks, input chunks to db
        while True: 
                t_start = time()        
                df = next(df_iter)      
                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

                df.to_sql(name=table_name, con=engine, if_exists='append')      
                t_end = time()  
                print('inserted another chunk, took %.3f second' % (t_end - t_start))




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


