import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

stations_file = sys.argv[1]
city_data_csv = sys.argv[2] 
plot_output = sys.argv[3]

stations = pd.read_json(stations_file, lines=True)
stations['avg_tmax'] = stations['avg_tmax']/10
# print(stations)

city_info = pd.read_csv(city_data_csv).dropna()
city_info['area'] = city_info['area']/1000000
city_info = city_info[city_info.area <= 10000]
city_info['density'] = city_info['population']/city_info['area']

# # The following code has been acquired from https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
def distance(city, stations):
    earth_radius = 6371
    lat_diff = np.radians(stations['latitude'] - city['latitude'])
    lon_diff = np.radians(stations['longitude'] - city['longitude'])

    a = np.square(np.sin(lat_diff/2)) + (np.cos(np.radians(city['latitude'])) * np.cos(np.radians(stations['latitude'])) * np.square(np.sin(lon_diff/2)))
    b = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return earth_radius * b

def best_tmax(city, stations):
    avg_tmax_all_stations = distance(city, stations)
    index_min_dis = pd.Series.idxmin(avg_tmax_all_stations)
    return stations.loc[index_min_dis]['avg_tmax']

city_info['best_tmax'] = city_info.apply(best_tmax, axis=1, stations=stations)
# print(city_info)

plt.plot(city_info['density'].values, city_info['best_tmax'].values, 'b.', alpha=0.5)
plt.show()
