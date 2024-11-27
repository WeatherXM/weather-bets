import requests
from decision import decide
import os
from datetime import datetime, timezone


def get_unix_timestamp(date_str, date_format="%Y-%m-%d"):
    dt = datetime.strptime(date_str, date_format)
    return int(dt.replace(tzinfo=timezone.utc).timestamp())

def fetch_events(namespace, limit, basin_base_url, after, before):
    url = f"{basin_base_url}/{namespace}/events"
    params = {
        "limit": limit,
        "after": after,
        "before": before
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    events = response.json()
    cids = [event['cid'] for event in events if 'cid' in event]
    return cids

def download_from_ipfs(cid, save_dir="downloads", gateway="http://localhost:8080/ipfs/"):
    """
    Download a file from IPFS locally.
    Args:
        cid (str): The IPFS Content Identifier (CID) of the file.
        save_dir: The directory where to save the fetched files from IPFS
        gateway (str): The IPFS gateway URL. Default is taken from environment variables.
    Returns:
        file_path: The file path where the file from IPFS is stored.
    """
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, cid)

    # If local node fails or not available, fallback to public IPFS gateway
    try:
        print(f"FALLBACK: FETCHING CID {cid} FROM IPFS GATEWAY")
        url = f"{gateway}/{cid}"
        response = requests.get(url,stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print(f"DOWNLOADED FILE TO {file_path} FROM LOCAL IPFS GATEWAY.")
            return file_path
        else:
            print(f"FAILED TO DOWNLOAD {cid}. HTTP STATUS: {response.status_code}")
    except Exception as e:
        print(f"ERROR DOWNLOADING FROM IPFS GATEWAY: {str(e)}")
        

def download_from_basin(cid, save_dir="downloads"):
    """
    Download a file from Basin using its CID and save it locally.
    Args:
        cid (str): The CID of the file to download.
        save_dir (str): The directory to save the downloaded file.
    Returns:
        str: The local file path where the file is saved.
    Raises:
        Exception: If the download fails.
    """
    base_url = f"https://basin.tableland.xyz/events/{cid}"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{cid}.parquet") 

    try:
        print(f"DOWNLOADING CID {cid}")
        response = requests.get(base_url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"FILE DOWNLOADED AND SAVED TO {file_path}")
        return file_path

    except requests.exceptions.RequestException as e:
        print(f"Failed to download CID {cid}: {e}")
        raise Exception(f"Error downloading file from Basin: {e}")
    
if __name__ == "__main__":
    namespace = os.getenv('BASIN_NAMESPACE')
    limit = 100

    after_date = os.getenv('AFTER') 
    before_date = os.getenv('BEFORE') 
    basin_base_url = os.getenv('BASIN_API_BASE_URL')

    after = get_unix_timestamp(after_date)
    before = get_unix_timestamp(before_date)
    gateway = os.getenv("IPFS_GATEWAY", "https://ipfs.io/ipfs")
    
    print(f"FETCHING CIDS FROM {after_date} ({after}) TO {before_date} ({before})")

    try:
        cids = fetch_events(namespace, limit, basin_base_url, after=after, before=before)
        print(f"RETRIEVED {len(cids)} CIDs FROM BASIN.")
        results = []
        for cid in cids:
            path = download_from_basin(cid)
            print(f"RECEIVED PATH FOR {cid}")
            decision = decide(path, True)
            # REMOVE FILE AFTER PROCESSING IT AND DOWNLOAD THE NEXT ONE
            os.remove(path)
            if type(decision) != str:
                results.append(int(decision))
        print('AVG TEMP: {} Celsius'.format(sum(results) / len(results)))

    except Exception as e:
        print(f"An error occurred: {e}")
