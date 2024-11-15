import pandas as pd
import numpy as np
import mne
from pathlib import Path
import matplotlib.pyplot as plt

def load_and_visualize_lsl_eeg(csv_file_path, sfreq=250):
    """
    Load EEG data from LSL-generated CSV file and visualize it using MNE-Python.
    Includes time-based topographic mapping.
    """
    # Load and prepare data
    data_df = pd.read_csv(csv_file_path)
    eeg_columns = [col for col in data_df.columns if col.startswith('EEG_')]
    data = data_df[eeg_columns].values.T
    
    # Define standard 8-channel positions
    ch_names = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2']
    ch_types = ['eeg'] * len(ch_names)
    
    # Create MNE objects
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    raw = mne.io.RawArray(data, info)
    montage = mne.channels.make_standard_montage('standard_1020')
    raw.set_montage(montage)
    
    print("\n=== Visualization Guide ===")
    
    # Raw signal plot
    print("\n1. Raw Signal Plot:")
    print("- Shows time-domain EEG signals for each channel")
    raw.plot(
        scalings='auto',
        title='Raw EEG Signals',
        show=True,
        block=False
    )
    
    # PSD plot
    print("\n2. Power Spectral Density Plot:")
    print("- Shows frequency content of each channel")
    raw.plot_psd(
        average=True,
        picks='eeg',
        spatial_colors=True,
        show=True
    )
    
    # Time-based topographic maps
    print("\n3. Topographic Maps Over Time:")
    print("- Shows spatial distribution of brain activity over time")
    print("- Each subplot represents a different time point")
    print("- Red/warmer colors: Higher activity")
    print("- Blue/cooler colors: Lower activity")
    
    # Calculate number of time points to show
    duration = len(data_df) / sfreq
    n_timepoints = 6  # Number of timepoints to display
    times = np.linspace(0, duration-1, n_timepoints)
    
    # Create figure for topomaps
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    
    # Get the data and plot topomaps
    data = raw.get_data()
    for idx, time in enumerate(times):
        time_idx = int(time * sfreq)
        mne.viz.plot_topomap(
            data[:, time_idx], 
            raw.info, 
            axes=axes[idx],
            show=False
        )
        axes[idx].set_title(f'Time: {time:.1f}s')
    
    plt.suptitle('EEG Topography at Different Time Points')
    plt.tight_layout()
    plt.show()
    
    # Create averaged topographic maps
    print("\n4. Averaged Topographic Maps:")
    print("- Shows average activity patterns across time ranges")
    
    # Create time windows for averaging (e.g., every 2 seconds)
    window_size = 2  # seconds
    n_windows = min(6, int(duration // window_size))  # Limit to 6 windows
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    
    for i in range(n_windows):
        start_time = i * window_size
        end_time = (i + 1) * window_size
        
        # Extract data for this time window
        start_idx = int(start_time * sfreq)
        end_idx = int(end_time * sfreq)
        data_window = raw.get_data(start=start_idx, stop=end_idx)
        data_avg = np.mean(data_window, axis=1)
        
        # Plot averaged topomap for this window
        mne.viz.plot_topomap(
            data_avg, 
            raw.info,
            axes=axes[i],
            show=False
        )
        axes[i].set_title(f'{start_time:.1f}-{end_time:.1f}s')
    
    # Remove any empty subplots
    for i in range(n_windows, len(axes)):
        fig.delaxes(axes[i])
    
    plt.suptitle('Average EEG Topography Across Time Windows')
    plt.tight_layout()
    plt.show()
    
    return raw

def process_and_analyze_lsl_eeg(raw):
    """
    Process EEG data and generate time-frequency analysis.
    """
    print("\n=== Processing and Analysis Guide ===")
    
    # Apply bandpass filter
    raw_filtered = raw.copy().filter(l_freq=1, h_freq=40)
    
    print("\n1. Time-Frequency Analysis:")
    print("- Shows how frequency content changes over time")
    
    # Calculate band power over time
    bands = {
        'Delta': (2, 4),
        'Theta': (4, 7),
        'Alpha': (8, 12),
        'Beta': (16, 25),
        'Gamma': (30, 50)
    }
    
    # Plot band power over time
    fig, axes = plt.subplots(len(bands), 1, figsize=(15, 12), sharex=True)
    times = raw_filtered.times
    
    for ax, (band_name, (fmin, fmax)) in zip(axes, bands.items()):
        # Calculate band power
        band_power = raw_filtered.copy()
        band_power.filter(l_freq=fmin, h_freq=fmax, picks='eeg')
        data = band_power.get_data()
        power = np.mean(data**2, axis=0)
        
        # Plot
        ax.plot(times, power)
        ax.set_title(f'{band_name} Band ({fmin}-{fmax} Hz) Power Over Time')
        ax.set_ylabel('Power')
    
    axes[-1].set_xlabel('Time (s)')
    plt.tight_layout()
    plt.show()
    
    return raw_filtered

if __name__ == "__main__":
    csv_file = "C:\\Users\\sonny\\OneDrive\\Documents\\Neurotech Club\\Cloned Repo\\NDML-DC\\csv_downloads\\P001\\S001\\WarmUp\\trial_00\\WarmUp_test_data.csv"
    data_df = pd.read_csv(csv_file)
    
    print("Loading and visualizing EEG data...")
    raw_eeg = load_and_visualize_lsl_eeg(csv_file_path=csv_file, sfreq=250)
    
    if raw_eeg is not None:
        print("\nProcessing EEG data...")
        processed_eeg = process_and_analyze_lsl_eeg(raw_eeg)