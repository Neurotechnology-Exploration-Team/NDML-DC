import numpy as np
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
from scipy.signal import butter, filtfilt
import sys
from brainflow.data_filter import DataFilter, FilterTypes
# Assuming your CSV data is saved in 'eeg_data.csv'



def preprocess_data(df, channels, lowcut=1.0, highcut=50.0, fs=1, order=5):
    """
    Preprocess EEG data: remove zeros and apply a bandpass filter to specified channels.

    Parameters:
    - df: DataFrame containing the EEG data and labels.
    - channels: List of channel names (strings) to preprocess.
    - lowcut: Low frequency for the bandpass filter.
    - highcut: High frequency for the bandpass filter.
    - fs: Sampling frequency.
    - order: Order of the bandpass filter.
    """
    # Copy DataFrame to avoid modifying the original data
    preprocessed_df = df.copy()

    for channel in channels:
        # Replace zeros with NaN to avoid affecting the filter
        preprocessed_df[channel] = preprocessed_df[channel].replace(0, np.nan)
        # Apply the filter only to non-NaN values
        valid_values = ~preprocessed_df[channel].isna()
        if valid_values.any():  # Check if there are any non-NaN values to filter
            data = preprocessed_df.loc[valid_values, channel].to_numpy()
            DataFilter.perform_bandpass(data, fs, lowcut, highcut, order, FilterTypes.BUTTERWORTH.value, 0)
            preprocessed_df.loc[valid_values, channel] = data

    return preprocessed_df


class DynamicEEGPlotter:
    def __init__(self, dataframe, channels, sampleinterval=0.05, timewindow=5.):
        self.df = dataframe
        self.channels = channels  # Now channels is a list of channel names
        self.sampleinterval = sampleinterval
        self.timewindow = timewindow

        # Initialize PyQt application
        self.app = QtWidgets.QApplication(sys.argv)
        self.win = pg.GraphicsLayoutWidget(show=True, title="Multi-Channel EEG Data Visualization")
        self.plot = self.win.addPlot(title='Real-time EEG Data')
        self.plot.setYRange(-150, 150)

        # Create a curve for each channel
        self.curves = []
        for channel in channels:
            curve = self.plot.plot(pen=pg.mkPen(width=2))
            self.curves.append(curve)

        # Vertical line to indicate current time or event
        self.verticalLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('white', width=2))
        self.plot.addItem(self.verticalLine)

        # Initialize data buffers for each channel
        self.databuffers = [np.zeros(int(timewindow / sampleinterval)) for _ in channels]
        self.x = np.linspace(-timewindow, 0.0, len(self.databuffers[0]))
        self.y = [np.zeros(len(self.databuffers[0])) for _ in channels]

        # Row index for DataFrame iteration
        self.row_index = 0

        # QTimer for updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(int(sampleinterval * 1000))

    def update(self):
        if self.row_index < len(self.df):
            for i, channel in enumerate(self.channels):
                new_value = self.df.iloc[self.row_index][channel]
                if not np.isnan(new_value):  # Assuming preprocessing to remove or mark zeros as NaN
                    self.databuffers[i] = np.roll(self.databuffers[i], -1)
                    self.databuffers[i][-1] = new_value
                    self.y[i] = self.databuffers[i]
                    self.curves[i].setData(self.x, self.y[i])

            # Optionally update the vertical line to indicate a new data point or event
            self.verticalLine.setPos(self.x[-1])

            self.row_index += 1
        else:
            # Reset for continuous demonstration or handle the end of the data
            self.row_index = 0

    def run(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtWidgets.QApplication.instance().exec_()


if __name__ == "__main__":
    df = pd.read_csv('./csv_downloads/P001/S002/Blink/trial_00/EEG_data.csv', index_col='Timestamp', parse_dates=True)
    channels = ['EEG_1', 'EEG_2', 'EEG_3', 'EEG_4', 'EEG_5', 'EEG_6', 'EEG_7', 'EEG_8']
    preprocessed_df = preprocess_data(df, channels)  # Assuming preprocess_data is defined and used as previously shown

    # Initialize and run the plotter for all channels
    plotter = DynamicEEGPlotter(preprocessed_df, channels=channels)
    plotter.run()
