import mne
import pandas as pd

def visualize_eeg_data(csv_file):
    # Read the EEG data from the CSV file
    data = pd.read_csv(csv_file)
    
    # Select only the EEG data columns
    eeg_data = data.iloc[:, 2:]  # Assuming the EEG data starts from the 3rd column
    
    # Create an MNE Raw object from the data
    ch_names = [f'Channel {i}' for i in range(1, 9)]  # Assuming 8 channels
    ch_types = ['eeg'] * 8
    sfreq = 1000  # Sampling frequency (you may need to adjust this)
    info = mne.create_info(ch_names, sfreq, ch_types)
    raw = mne.io.RawArray(eeg_data.values.T, info)
    
    # Plot the EEG data
    raw.plot()
visualize_eeg_data('C:\\Users\\sonny\\OneDrive\\Documents\\Neurotech Club\\Cloned Repo\\NDML-DC\\csv_downloads\\P001\\S001\\WarmUp\\trial_00\\WarmUp_test_data.csv')