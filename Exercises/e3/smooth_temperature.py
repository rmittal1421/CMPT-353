import sys
import numpy as np
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess
import matplotlib.pyplot as plt
from pykalman import KalmanFilter

filename = sys.argv[1]

def to_timestamp (date):
    return date.timestamp()

cpu_data = pd.read_csv(filename, parse_dates=[4])

plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)

cpu_data['timestamp_formatted'] = cpu_data['timestamp'].apply(to_timestamp)

loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp_formatted'], frac=0.004)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')

kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1']]
initial_state = kalman_data.iloc[0]
observation_covariance = np.diag([2, 0.004, 0.06]) ** 2 
transition_covariance = np.diag([1, 0.004, 0.06]) ** 2 
transition = [[1.0, -1.0, 0.7], [0, 0.6, 0.03], [0, 1.3, 0.8]] 

kf = KalmanFilter(
        initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition
)
kalman_smoothed, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
plt.legend(['Data points', 'LOESS-smoothed line', 'Kalman-smoothed line'])
plt.xlabel('timestamp')
plt.ylabel('cpu_temperature')
plt.savefig('cpu.svg')