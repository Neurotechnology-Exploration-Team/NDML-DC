# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1-b] - 2/19/2024

### Fixed
- Abort button causing issues with the display canvas.

## [1.1.0-b] - 2/17/2024

### Added
- A timer displaying the elapsed time of the test to the top of the control window.

## [1.0.0-b] - 2/16/2024
> **THE TEST RELEASE** - all tests are now accurate and working to IRB specification.

### Added
- All test image assets
- Abort test button
- Audio cues for blinking and transition tests
- Several new test timing variables to config

### Changed
- Changed from each test having its own class to a template-based test system:
  - All tests extend a base `TestThread` class
  - `BlinkTest`, `ConstantTest`, and `TransitionTest` are three different test types with three different behaviors
- Timestamps are now a constant millisecond value from an arbitrary point.
  - See [the LSL documentation](https://labstreaminglayer.readthedocs.io/info/faqs.html?highlight=timestamp#lsl-local-clock) for the reasoning behind this.

### Fixed
- All test images now appear with transparent backgrounds
- Labeling in saved CSV files

### Removed
- `postprocessing` module as we no longer display graphs after collection

## [4.4.1-a] - 2/5/2024

### Fixed
- Timestamps of the collected data have been updated to match up with the exact millisecond the data is recorded
  - Format of how the timestamps were being written to the CSV file has been modified

## [4.4.0-a] - 2/5/2024

### Added
- Exit test button that handles all exit behavior.

### Fixed
- Fixed broken graph zooming on Unix-based systems.
- Fixed **all** window closing behaviors causing issues with the test lifecycle.

### Removed
- Fullscreen mode config flag

## [4.3.1-b] - 2/05/2024
### Added
  - The following Test Cases have been added
    - Brow Frowed to Unfrowed
    - Brow Frowed
    - Brow Unfrowed
    - Eyes Open to Eyes Closed
    - Eyes Closed
    - Eyes Opened
    - Float Down/ Up / Left / Right
    - Selection
    - Stationary Float
    - Stationy Float to Float Down/ Float Up /Float Right / Float Left
   
  - Added Dynamic timing for test duration based on type of test being conducted.


## [4.3.1-a] - 1/31/2024

### Fixed
- Timestamps derived from LSL stream now match up to system time using an updated offset from pylsl.
  - The precision of these estimates should be below 1 ms (empirically within +/-0.2 ms).

## [4.3.0-a] - 1/31/2024

### Added
- Two new configuration variables in `config.py`:
  - Ability to enable/disable supported stream types
  - Variable duration of blinking text

### Changed
- The collector now stores and collects data on a per-stream basis
- LSL data is now stored in separate stream CSVs (i.e. `EEG_data.csv`), removing any 0 or NaN data points from misaligned sampling.

## [4.2.0-a] - 1/31/2024

### Added
- Postprocessing bandpass filtering to reduce noise in displayed EEG graphs.

## [4.1.0-a] - 1/29/2024

### Added
- Prompt for session number on startup

### Changed
- Renamed all references from "subject" to "participant"
- Changed participant folder structure to include session number
  - Stored as `<DATA_PATH>/PXXX/SXXX/trial_XX/<STREAM_TYPE>_date.csv`

## [4.0.1-a] - 1/25/2024

### Fixed
- Fixed trial number hardcoded as 1.

## [4.0.0-a] - 1/25/2024

### Added
- Test state tracking in `TestGUI` to implement trial numbers and test completed status.
- Exit application when all tests are complete
- Data now saves to `DATA_PATH/<id>/<test>/trial_<trial_number>/FILENAME` (see [config.py](../config.py) for additional configuration)

### Changed
- Refactored `Blink` (example test) into `Action` with more customizable parameters for blinking text.
  - This will probably need to be updated in the future for more test variety

### Added
- Image assets for GUI tests

## [3.2.0-a] - 1/25/2024

### Added
- Image assets for GUI tests

## [3.1.0-a] - 1/17/2024

### Added
- Popup when initializing GUI to prompt for the subject number.

## [3.0.0-a] - 1/16/2024

### Added

- `config` file in the repository root directory that holds all experiment/collection constants.
- Button colors to indicate test status

### Changed

- Changed `tests` package to a class-based system that uses Python's default `Thread` class.
  - Each test is now a class that extends the `TestThread` class, which holds logic that applies to all tests.
  - Moved all Tkinter logic into `tests/TestGUI` static class.
- Converted `LSL` module to a static class.
- Labelling is now performed entirely in the `LSL` class

### Fixed
- Multiple confirmation window bugs

## [2.0.0-a] - 1/9/2024

### Added

- Lots of docstrings, documentation, code cleanup, etc.

### Changed

- Changed `lsl.py` module to the `LSL.py` class, allowing for one instance of LSL to manipulate.
- Moved most constants to the top-level of relevant modules.

## [1.0.1-a] - 1/9/2024

### Changed

- Update `requirements.txt` to be the minimum required packages to install.

## [1.0.0-a] - 1/9/2024

### Added

- `changelog.md` to keep track of changes.
- All LSL & post-processing functionality.
- Tests using Tkinter windows.

### Fixed

- No LSL stream would hang up the program instead of exiting.

### Changed

### Removed

