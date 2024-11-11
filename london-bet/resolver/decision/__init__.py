import pyarrow.parquet as pq
import pandas as pd
import location.algo as location
import weather.algo as weather
import data.algo as data


def from_file(path):
    return pq.read_pandas(path, columns=['name', 'model', 'cell_id', 'public_key', 'ws_packet_b64', 'ws_packet_sig', 'lat', 'lon', 'qod_score', 'pol_score', 'temperature']).to_pandas()

def load_df(path, low_mem):
    if low_mem:
        print('LOADING WITH CHUNKS')
        parquet_file = pq.ParquetFile(path)
        processed_chunks = []
        for i in range(0, parquet_file.metadata.num_row_groups):
            chunk = parquet_file.read_row_group(i).to_pandas(use_threads=True)
            chunk = chunk[['name', 'model','cell_id', 'public_key', 'ws_packet_b64', 'ws_packet_sig', 'lat', 'lon', 
                        'qod_score', 'pol_score', 'temperature']]
            chunk = chunk.astype({
                'name': 'category',
                'model': 'category',
                'cell_id': 'category',
                'public_key': 'category',
                'ws_packet_b64': 'category',
                'ws_packet_sig': 'category',
                'lat': 'float32',
                'lon': 'float32',
                'qod_score': 'float32',
                'pol_score': 'int8',  
                'temperature': 'float32'
            })
            processed_chunk = filter(chunk)
            processed_chunks.append(processed_chunk)
        df = pd.concat(processed_chunks, ignore_index=True)
    else:
        print('LOADING WITHOUT CHUNKS')
        df_loaded = from_file(path)
        df = filter(df_loaded)
    return df

def filter(chunk):
    geo_filtered = location.geo_filter(chunk)
    print('GEO VERIFIED DEVICES COUNT: {}'.format(len(geo_filtered['name'].unique())))
    print('GEO LOCATION VERIFICATION IS COMPLETED')     
    weather_verified = weather.has_verified_metrics(geo_filtered)
    print('WEATHER VERIFIED DEVICES COUNT WITH QOD>=0.8 AND POL==1: {}'.format(len(weather_verified['name'].unique())))
    print('WEATHER DATA FILTERING IS COMPLETED')     
    data_verified = data.verify(weather_verified)
    print('DATA VERIFICATION IS COMPLETED')
    print('DATA VERIFIED DEVICES COUNT: {}'.format(len(data_verified['name'].unique())))
    print('LONDON DEVICES PARTICIPATING IN BET RESOLUTION AFTER FILTERING {}%'.format(round((len(data_verified['name'].unique()) * 100)/len(geo_filtered['name'].unique())),8))
    return data_verified

def decide(path, low_mem):
    df = load_df(path, low_mem)
    device_mean = df.groupby('name', as_index=False, observed=False)['temperature'].mean()
    london_temp_mean = device_mean.rename(columns={'temperature': 'mean'})['mean'].mean()
    return london_temp_mean


