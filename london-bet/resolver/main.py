import argparse
from decision import decide
import weather.algo as weather

parser = argparse.ArgumentParser(description='Decide if an event occurred based on weather data provided as input')
parser.add_argument('--file', '-f', required=True, help='the file with the weather data')
parser.add_argument('--lowmem', '-lowmem', required=True, type=bool, help='use limited memory resources or not')
parser.add_argument('--latitude', '-lat', required=False, type=float, help='the latitude of the point of interest (search within 5km radius)')
parser.add_argument('--longitude', '-lon', required=False, type=float, help='the longitude of the point of interest (search within 5km radius)')


args = parser.parse_args()
path, lowmem, lat, lon = args.file, args.lowmem args.latitude, args.longitude
algo = weather.has_verified_metrics
decision = decide(path, algo, lowmem, lat, lon)
print(decision)


