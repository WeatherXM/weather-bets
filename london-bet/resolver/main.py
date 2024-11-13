import argparse
from decision import decide

parser = argparse.ArgumentParser(description='Decide if an event occurred based on weather data provided as input')
parser.add_argument('--file', '-f', required=True, help='the file with the weather data')
parser.add_argument('--lowmem', '-lm', required=False, type=bool, help='use limited memory resources or not')
parser.add_argument('--latitude', '-lat', required=False, type=float, help='the latitude of the point of interest (search within 5km radius)')
parser.add_argument('--longitude', '-lon', required=False, type=float, help='the longitude of the point of interest (search within 5km radius)')


args = parser.parse_args()
path, lowmem, lat, lon = args.file, args.lowmem, args.latitude, args.longitude
decision = decide(path, lowmem)
print('AVG TEMP: {} Celsius'.format(decision))


