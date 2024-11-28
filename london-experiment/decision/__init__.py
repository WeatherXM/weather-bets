import pyarrow.parquet as pq
import pandas as pd
import location.algo as location
import weather.algo as weather
import data.algo as data
import numpy as np


def from_file(path):
    return pq.read_pandas(path, columns=['name', 'model', 'cell_id', 'public_key_PEM', 'ws_packet_b64', 'ws_packet_sig', 'lat', 'lon', 'qod_score', 'pol_score', 'temperature']).to_pandas()

def load_df(path, low_mem):
    chunk_num = 0
    if low_mem:
        print('LOADING WITH CHUNKS')
        parquet_file = pq.ParquetFile(path)
        processed_chunks = []
        for i in range(parquet_file.metadata.num_row_groups):
            chunk = parquet_file.read_row_group(i).to_pandas(use_threads=True)
            chunk = chunk[['name', 'model', 'cell_id', 'public_key_PEM', 'ws_packet_b64', 
                        'ws_packet_sig', 'lat', 'lon', 'qod_score', 'pol_score', 'temperature']]
            chunk = chunk.astype({
                'name': 'category',
                'model': 'string',
                'cell_id': 'string',
                'public_key_PEM': 'string',
                'ws_packet_b64': 'string',
                'ws_packet_sig': 'string',
                'lat': 'float32',
                'lon': 'float32',
                'qod_score': 'float32',
                'pol_score': 'float32',
                'temperature': 'float32'
            })
            filtered_chunk = filter(chunk)
            chunk_num += 1
            if not filtered_chunk.empty:
                print(f"Processed chunk {i}: {filtered_chunk.shape[0]} rows")
                processed_chunks.append(filtered_chunk)
            else:
                print(f"CHUNK {i} WAS FILTERED OUT (NO ROWS MEET THE FILTERING CRITERIA)")
        if processed_chunks:
            df = pd.concat(processed_chunks, ignore_index=True)
            print("FINAL DATAFRAME SHAPE:", df.shape)
        else:
            df = pd.DataFrame(columns=['name', 'model', 'cell_id', 'public_key_PEM', 
                                    'ws_packet_b64', 'ws_packet_sig', 'lat', 'lon', 
                                    'qod_score', 'pol_score', 'temperature'])
            print("NO ROWS MET THE FILTERING CRITERIA")
    else:
        print('LOADING WITHOUT CHUNKS')
        df_loaded = from_file(path)
        df = filter(df_loaded)
        chunk_num = 1
    return df, chunk_num

def filter(chunk):
    chunk_pol_cleaned = chunk[np.isfinite(chunk['pol_score'])]
    chunk_cleaned = chunk_pol_cleaned[np.isfinite(chunk_pol_cleaned['qod_score'])]
    geo_filtered = location.geo_filter(chunk_cleaned)
    print('GEO VERIFIED DEVICES COUNT: {}'.format(len(geo_filtered['name'].unique())))
    print('GEO LOCATION VERIFICATION IS COMPLETED')
    weather_verified = weather.has_verified_metrics(geo_filtered)
    print('WEATHER VERIFIED DEVICES COUNT WITH QOD>=0.8 AND POL>0: {}'.format(len(weather_verified['name'].unique())))
    print('WEATHER DATA FILTERING IS COMPLETED')     
    data_verified = data.verify(weather_verified)
    print('DATA VERIFICATION IS COMPLETED')
    print('DATA VERIFIED DEVICES COUNT: {}'.format(len(data_verified['name'].unique())))
    if geo_filtered.size>0:
        print('LONDON DEVICES FROM DATAFRAME PARTICIPATING IN BET RESOLUTION AFTER FILTERING: {}%'.format(round((len(data_verified['name'].unique()) * 100)/len(geo_filtered['name'].unique())),8))
    return data_verified

def decide(path, low_mem):
    df,chunk_num = load_df(path, low_mem)
    print("PROCESSED {} CHUNKS FOR FILE {}".format(chunk_num,path))
    if df.size>0:
        device_mean = df.groupby('name', as_index=False, observed=False)['temperature'].mean()
        london_temp_mean = device_mean.rename(columns={'temperature': 'mean'})['mean'].mean()
        return round(london_temp_mean,2)
    return 'NO DEVICES MEET THE CRITERIA TO CALCULATE AVG TEMPERATURE'


