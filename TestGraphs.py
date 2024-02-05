import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
from scipy.stats import zscore
import sys
from brainflow.data_filter import DataFilter, FilterTypes
def preprocess_and_normalize(df, channels, exclude_initial_samples=0, z_thresh=3,retain_peaks = True):
    """
    Preprocess and normalize EEG data, excluding outliers.

    Parameters:
    - df: DataFrame with EEG data.
    - channels: Channels to preprocess.
    - exclude_initial_samples: Number of initial samples to exclude as outliers.
    - z_thresh: Z-score threshold for identifying outliers.
    """
    processed_df = df.copy()

    # Optionally exclude initial samples known to be outliers
    if exclude_initial_samples > 0:
        processed_df = processed_df.iloc[exclude_initial_samples:]

    for channel in channels:
        # Optionally adjust this part to better retain peaks
        if retain_peaks:
            # Example: Apply a less aggressive normalization or a different preprocessing approach
            processed_df[channel] = (processed_df[channel] - np.mean(processed_df[channel])) / np.std(
                processed_df[channel])
        else:
            # Apply z-score to identify outliers
            z_scores = zscore(processed_df[channel])
            abs_z_scores = np.abs(z_scores)

            # Exclude outliers based on z-score threshold
            filtered_entries = (abs_z_scores < z_thresh)
            processed_df = processed_df[filtered_entries]

            # Normalize data (mean=0, std=1)
            processed_df[channel] = (processed_df[channel] - processed_df[channel].mean()) / processed_df[channel].std()

    return processed_df


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

class DynamicEEGPlotter:
    def __init__(self, dataframe, channels, sampleinterval=0.05, timewindow=5.):
        self.df = dataframe  # Assuming the dataframe is already preprocessed
        self.channels = channels
        self.sampleinterval = sampleinterval
        self.timewindow = timewindow
        self.blink_markers = []
        self.app = QtWidgets.QApplication(sys.argv)

        self.win = pg.GraphicsLayoutWidget(show=True, title="Multi-Channel EEG Data Visualization")
        self.plot = self.win.addPlot(title='Real-time EEG Data')
        self.plot.setYRange(-150, 150)

        self.curves = []
        for _ in channels:
            curve = self.plot.plot(pen=pg.mkPen(width=2))
            self.curves.append(curve)

        self.databuffers = [np.zeros(int(self.timewindow / self.sampleinterval)) for _ in channels]
        self.x = np.linspace(-self.timewindow, 0.0, len(self.databuffers[0]))

        self.row_index = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(int(self.sampleinterval * 1000))

    def update(self):
        if self.row_index < len(self.df):
            for marker in self.blink_markers:
                self.plot.removeItem(marker)
            self.blink_markers.clear()

            for i, channel in enumerate(self.channels):
                new_value = self.df.iloc[self.row_index][channel]
                label = self.df.iloc[self.row_index]['Label']
                if not pd.isna(new_value):
                    self.databuffers[i] = np.roll(self.databuffers[i], -1)
                    self.databuffers[i][-1] = new_value
                    self.curves[i].setData(self.x, self.databuffers[i], pen=pg.mkPen('g', width=2))
                    if label == 'Blink':
                        marker = self.plot.plot([self.x[-1]], [new_value], symbol='o', symbolSize=5, symbolBrush='r',
                                                pen=None)
                        self.blink_markers.append(marker)

            self.row_index += 1
        else:
            self.row_index = 0

    def run(self):
        QtWidgets.QApplication.instance().exec_()

if __name__ == "__main__":
    # Assuming preprocess_and_normalize is defined as shown earlier
    df = pd.read_csv('./csv_downloads/P001/S002/Blink/trial_00/EEG_data.csv', index_col='Timestamp', parse_dates=True)
    channels = ['EEG_1']  # Specify the channels you're interested in

    # Apply preprocessing and normalization
    #preprocessed_df = preprocess_and_normalize(df, channels)
    scaled_df = scale_data_to_range(df, channels, min_val=-200, max_val=200)

    # Initialize and run the plotter with the scaled data
    plotter = DynamicEEGPlotter(scaled_df, channels=channels)
    plotter.run()