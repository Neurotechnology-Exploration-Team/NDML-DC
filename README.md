# NXT Data Collector
> This project houses the code to prompt the user in a Tkinter window, store, and process brain wave EEG data from an LSL stream.

## Download & Install

### Git 
```bash
$ git clone https://github.com/Neurotechnology-Exploration-Team/DataCollector.git
$ cd DataCollector/
$ pip install -r requirements.txt
```

### OpenBCI GUI
> This is required to interact with LSL stream data.

Install the latest version of the [Standalone OpenBCI GUI](https://openbci.com/downloads) (v5.2.2)


## Usage
> You will first need to setup LSL streams for the Data Collector to interface with.

### LSL Streaming

1. Launch `OpenBCI_GUI.exe`
2. Select data source type from from `System Control Panel > DATA SOURCE`.
   1. **Algorithmic LSL Data (Testing):** Select **`SYNTHETIC (Algorithmic)`** 
   2. ***TODO*** **Real-Time LSL Data:** Select **`CYTON (Live)`**
3. Leave all settings as default, and press `START SESSION`

4. Change the bottom right widget to `Networking`
   1. Change protocol to `LSL`
   2. Screenshot here
   3. Press `Start LSL Stream` to activate the LSL stream on the local network.
5. Press `Start Data Stream` to begin streaming test data.

> The data is now streaming. Press `Stop Data Stream` when complete.

### Data Collection
> Once the LSL streams have been established, the data collection process can be initiated

Run main.py to run all tests and record data
```bash
$ python main.py
```

## Contributors
**Principal Investigator:** [Alex Burbano](mailto:arb8590@rit.edu)

**Research Team:**
- [Ian Dunn](mailto:itd3516@rit.edu)