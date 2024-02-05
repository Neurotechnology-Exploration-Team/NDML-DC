import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
from scipy.stats import zscore
import sys
from brainflow.data_filter import DataFilter, FilterTypes, NoiseTypes


def preprocess_eeg_data(df, channel, fs=250, band_start=5, band_stop=50, notch_start=50, notch_stop=60, filter_order=4):
    """
    Preprocess EEG data for a specific channel: Apply bandpass and notch filters.

    Parameters:
    - df: DataFrame containing the EEG data.
    - channel: The channel name (string) to preprocess.
    - fs: Sampling frequency of the EEG data.
    - band_start: Start frequency for the bandpass filter.
    - band_stop: Stop frequency for the bandpass filter.
    - notch_start: Start frequency for the notch filter.
    - notch_stop: Stop frequency for the notch filter.
    - filter_order: Order of the Butterworth filter.
    """
    data = df[channel].to_numpy().flatten()

    # Apply bandpass filter
    DataFilter.perform_bandpass(data, fs, band_start, band_stop, filter_order, FilterTypes.BUTTERWORTH.value, 0)

    # Apply notch filter to remove power line noise
    DataFilter.perform_bandstop(data, fs, notch_start, notch_stop, filter_order, FilterTypes.BUTTERWORTH.value, 0)

    return data


def scale_data_to_range(df, channels, min_val=-200, max_val=200):
    """
    Scale EEG data to fit within a specified range for each channel.

    Parameters:
    - df: DataFrame containing the EEG data.
    - channels: List of channel names (strings) to preprocess.
    - min_val: Minimum value of the desired range.
    - max_val: Maximum value of the desired range.
    """
    scaled_df = df.copy()

    for channel in channels:
        # Extract the channel data
        channel_data = scaled_df[channel]

        # Find the min and max of the current data
        data_min = channel_data.min()
        data_max = channel_data.max()

        # Scale the data to fit the new range
        scaled_data = (channel_data - data_min) / (data_max - data_min) * (max_val - min_val) + min_val

        # Replace the original data with scaled data
        scaled_df[channel] = scaled_data

    return scaled_df


def scale_data_to_global_range(df, channels, min_val=-200, max_val=200):
    """
    Scale EEG data to fit within a specified global range across all channels.

    Parameters:
    - df: DataFrame containing the EEG data.
    - channels: List of channel names (strings) to preprocess.
    - min_val: Minimum value of the desired range.
    - max_val: Maximum value of the desired range.
    """
    scaled_df = df.copy()

    # Determine the global min and max across all specified channels
    global_min = df[channels].min().min()
    global_max = df[channels].max().max()

    for channel in channels:
        # Scale the data to fit the new range using global min and max
        scaled_data = (df[channel] - global_min) / (global_max - global_min) * (max_val - min_val) + min_val

        # Replace the original data with scaled data
        scaled_df[channel] = scaled_data

    return scaled_df


class DynamicEEGPlotter:
    def __init__(self, data, sampleinterval=0.5, timewindow=100):
        self.data = data  # Preprocessed data for the channel as a NumPy array
        self.sampleinterval = sampleinterval
        self.timewindow = timewindow

        self.app = QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(show=True, title="EEG Data Visualization")
        self.plot = self.win.addPlot(title='Real-time EEG Data')
        self.plot.setYRange(-21, 21)  # Adjusted to the specified range of +21 µV to -21 µV

        # Initialize a single curve for plotting
        self.curve = self.plot.plot(pen=pg.mkPen(width=2))

        # Initialize the data buffer to store EEG data points for plotting
        self.databuffer = np.zeros(int(self.timewindow / self.sampleinterval))
        self.x = np.linspace(-self.timewindow, 0.0, len(self.databuffer))

        self.row_index = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(int(self.sampleinterval * 3))

    def update(self):
        if self.row_index < len(self.data):
            new_value = self.data[self.row_index]
            # Update the data buffer with the new value
            self.databuffer = np.roll(self.databuffer, -1)
            self.databuffer[-1] = new_value

            # Update the curve with new data
            self.curve.setData(self.x, self.databuffer)

            self.row_index += 1
        else:
            self.row_index = 0  # Optionally reset row_index or stop the timer

    def run(self):
        self.win.show()
        QtWidgets.QApplication.instance().exec_()

if __name__ == "__main__":
    # Assuming preprocess_and_normalize is defined as shown earlier
    df = pd.read_csv('./csv_downloads/P001/S002/Blink/trial_00/EEG_data.csv', index_col='Timestamp', parse_dates=True)
    channels = ['EEG_6']  # Specify the channels you're interested in

    # Apply preprocessing and normalization
    #preprocessed_df = preprocess_and_normalize(df, channels)
    #scaled_df = scale_data_to_global_range(df, channels, min_val=-200, max_val=200)

    preprocessed_df = preprocess_eeg_data(df, channels)
    # Initialize and run the plotter with the preprocessed data
    plotter = DynamicEEGPlotter(preprocessed_df)
    plotter.run()