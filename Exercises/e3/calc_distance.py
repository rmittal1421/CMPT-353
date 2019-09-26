import sys
import numpy as np
import pandas as pd
from xml.dom.minidom import parse
from pykalman import KalmanFilter

def get_data(filename):
    file = parse(filename)

    trkpt_elements = file.getElementsByTagName('trkpt')

    _lat = []
    _lon = []
    for elem in trkpt_elements:
        _lat.append(float(elem.getAttribute('lat')))
        _lon.append(float(elem.getAttribute('lon')))
    
    data = pd.DataFrame({'lat': _lat, 'lon': _lon})
    return data

# The following code has been acquired from https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
def getDistanceValue(points):
    earth_radius = 6371
    location_data = points.copy()
    location_data['rad_diff_lat'] = np.radians(location_data['lat2'] - location_data['lat'])
    location_data['rad_diff_lon'] = np.radians(location_data['lon2'] - location_data['lon'])

    a = np.square(np.sin(location_data['rad_diff_lat']/2)) + (np.cos(np.radians(location_data['lat'])) * np.cos(np.radians(location_data['lat2'])) * np.square(np.sin(location_data['rad_diff_lon']/2)))
    b = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    c = earth_radius * b
    return np.sum(c)

def distance(df):
    df_copy = df.copy()
    df_copy['lat2'] = df['lat'].shift(periods=-1)
    df_copy['lon2'] = df['lon'].shift(periods=-1)
    return 1000 * getDistanceValue(df_copy.dropna())

def smooth(points):
    initial_state = points.iloc[0]
    print(initial_state)
    observation_covariance = np.diag([0.0002, 0.0002]) ** 2 
    transition_covariance = np.diag([0.00015, 0.0001]) ** 2 
    transition = [[1, 0], [0, 1]] 

    kf = KalmanFilter(
            initial_state_mean=initial_state,
            initial_state_covariance=observation_covariance,
            observation_covariance=observation_covariance,
            transition_covariance=transition_covariance,
            transition_matrices=transition
    )
    kalman_smoothed, _ = kf.smooth(points)
    return pd.DataFrame(kalman_smoothed, columns=['lat', 'lon'])


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()