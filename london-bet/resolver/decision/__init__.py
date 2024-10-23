import pyarrow.parquet as pq
import pandas as pd
import location.algo as location
import weather.algo as weather


def from_file(path):
    return pq.read_pandas(path, columns=['name', 'cell_id', 'public_key', 'ws_packet_b64', 'ws_packet_sig', 'lat', 'lon', 'qod_score', 'pol_score', 'temperature']).to_pandas()

def load_df(path, low_mem):
    if low_mem:
        parquet_file = pq.ParquetFile(path)
        processed_chunks = []
        for i in range(0, parquet_file.metadata.num_row_groups):
            chunk = parquet_file.read_row_group(i).to_pandas(use_threads=True)
            chunk = chunk[['name', 'cell_id', 'public_key', 'ws_packet_b64', 'ws_packet_sig', 'lat', 'lon', 
                        'qod_score', 'pol_score', 'temperature']]
            chunk = chunk.astype({
                'name': 'category',
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
        df = from_file(path)
    return df

def filter(chunk):
    geo_filtered = location.geo_filter(chunk)
    data_verified = weather.has_verified_metrics(geo_filtered)
    return data_verified

def decide(path, algo, low_mem, lat, lon):
    df = load_df(path, low_mem)
    device_mean = df.groupby('name', as_index=False, observed=False)['temperature'].mean()
    london_temp_mean = device_mean.rename(columns={'temperature': 'mean'})['mean'].mean()
    return london_temp_mean


