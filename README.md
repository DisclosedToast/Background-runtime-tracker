# Application Runtime Tracker

This project is a background application that tracks when other applications are opened and closed, providing a summary of their runtime in hours.

## Features

- Monitors the opening and closing of applications.
- Summarizes the total runtime of each tracked application.
- Stores session data for persistent tracking.

## Project Structure

```
app-runtime-tracker
├── src
│   ├── main.py               # Entry point of the application
│   ├── process_tracker.py     # Monitors application processes
│   ├── runtime_summary.py      # Summarizes application runtimes
│   ├── models
│   │   └── process_session.py  # Represents a session of an application
│   └── services
│       └── storage.py         # Handles storage of session data
├── tests
│   ├── test_process_tracker.py # Unit tests for ProcessTracker
│   └── test_runtime_summary.py  # Unit tests for RuntimeSummary
├── requirements.txt           # Project dependencies
├── pyproject.toml            # Project configuration
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd app-runtime-tracker
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.